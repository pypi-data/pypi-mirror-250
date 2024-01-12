
import gzip
import io
import os
import struct
import numpy as np
import slideflow as sf
import asyncio
import aiofiles
import struct
import logging
import itertools

from typing import Dict, Iterable, List, Optional, Tuple, Union
from slideflow.tfrecord import iterator_utils
from slideflow.util import example_pb2, extract_feature_dict, tfrecord2idx, log

log = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

async def _async_read_data(file, length_bytes, crc_bytes, datum_bytes) -> memoryview:
    """Read the next record from the tfrecord file asynchronously."""
    if await file.readinto(length_bytes) != 8:
        raise RuntimeError("Failed to read the record size.")
    if await file.readinto(crc_bytes) != 4:
        raise RuntimeError("Failed to read the start token.")
    length, = struct.unpack("<Q", length_bytes)
    if length > len(datum_bytes):
        try:
            _fill = int(length * 1.5)
            datum_bytes = datum_bytes.zfill(_fill)
        except OverflowError:
            raise OverflowError('Overflow encountered reading tfrecords; please '
                                'try regenerating index files')
    datum_bytes_view = memoryview(datum_bytes)[:length]
    if await file.readinto(datum_bytes_view) != length:
        raise RuntimeError("Failed to read the record.")
    if await file.readinto(crc_bytes) != 4:
        raise RuntimeError("Failed to read the end token.")
    return datum_bytes_view

# -----------------------------------------------------------------------------

class AsyncTFRecordIterator:
    typename_mapping = {
            "byte": "bytes_list",
            "float": "float_list",
            "int": "int64_list"
        }

    def __init__(
        self,
        data_path: str,
        index: Optional[np.ndarray] = None,
        shard: Optional[Tuple[int, int]] = None,
        clip: Optional[int] = None,
        compression_type: Optional[str] = None,
        random_start: bool = False,
        datum_bytes: Optional[bytearray] = None,
    ) -> None:
        """Create an iterator over the tfrecord dataset.

        Since the tfrecords file stores each example as bytes, we can
        define an iterator over `datum_bytes_view`, which is a memoryview
        object referencing the bytes.

        Params:
        -------
        data_path: str
            TFRecord file path.

        index: optional, default=None
            np.loadtxt(index_path, dtype=np.int64)

        shard: tuple of ints, optional, default=None
            A tuple (index, count) representing worker_id and num_workers
            count. Necessary to evenly split/shard the dataset among many
            workers (i.e. >1).

        random_start: randomize starting location of reading.
            Requires an index file. Only works if shard is None.

        Yields:
        -------
        datum_bytes_view: memoryview
            Object referencing the specified `datum_bytes` contained in the
            file (for a single record).
        """

        # Replace file opening with aiofiles
        if compression_type == "gzip":
            raise NotImplementedError("Async gzip reading not implemented.")
        elif compression_type is None:
            self.file = None

        else:
            raise ValueError("compression_type should be 'gzip' or None")

        self.data_path = data_path
        self.shard = shard
        self.clip = clip
        self.random_start = random_start
        if datum_bytes is not None:
            self.datum_bytes = datum_bytes
        else:
            self.datum_bytes = bytearray(1024 * 1024)
        self.length_bytes = bytearray(8)
        self.crc_bytes = bytearray(4)
        self.index = index
        self.index_is_nonsequential = None
        if self.index is not None and len(self.index) != 0:
            # For the case that there is only a single record in the file
            if len(self.index.shape) == 1:
                self.index = np.expand_dims(self.index, axis=0)

            # Check if the index file contains sequential records
            self.index_is_nonsequential = (
                not np.all(np.cumsum(self.index[:, 1][:-1])
                           + self.index[0, 0] == self.index[:, 0][1:])
            )

            # Only keep the starting bytes for the indices
            self.index = self.index[:, 0]  # type: ignore

            # Ensure the starting bytes are in order
            self.index = np.sort(self.index)
        self.iterator = None

    async def _read_sequential_records(self, start_offset=None, end_offset=None):
        if start_offset is not None:
            await self.file.seek(start_offset)
        if end_offset is None:
            end_offset = os.path.getsize(self.data_path)
        while await self.file.tell() < end_offset:
            yield await self._read_next_data()

    async def _read_nonsequential_records(self, start_offset=None, end_offset=None):
        """Read nonsequential records from the given starting byte asynchronously.

        Only read records with starting bytes reflected in the index file.
        """
        if start_offset not in self.index:
            raise ValueError("Offset not in the tfrecord index.")
        if start_offset is None:
            start_offset = self.index[0]
            index_loc = 0
        else:
            index_loc = np.argwhere(self.index == start_offset)[0][0]

        if end_offset is None:
            end_offset = os.path.getsize(self.data_path)

        while self.index[index_loc] < end_offset:
            if await self.file.tell() != self.index[index_loc]:
                await self.file.seek(self.index[index_loc])

            yield await self._read_next_data()
            index_loc += 1

            # End the loop if we have reached the last index
            if index_loc >= len(self.index):
                break

    async def _read_next_data(self) -> memoryview:
        try:
            data = await _async_read_data(
                self.file,
                self.length_bytes,
                self.crc_bytes,
                self.datum_bytes
            )
        except Exception as e:
            log.error(f"Error reading data from tfrecord {self.data_path}: {e}")
            raise e
        try:
            return self.process(data)
        except Exception as e:
            log.error(f"Error processing data from tfrecord {self.data_path}: {e}")
            raise e

    async def read_records(self, start_offset=None, end_offset=None):
        if self.index_is_nonsequential:
            async for record in self._read_nonsequential_records(start_offset, end_offset):
                yield record
        else:
            async for record in self._read_sequential_records(start_offset, end_offset):
                yield record

    async def __aiter__(self):
        """Return an asynchronous iterator."""
        self.file = await aiofiles.open(data_path, 'rb')  # type: ignore
        if self.index is None:
            self.iterator = self.read_records()
        elif not len(self.index):
            self.iterator = iter([])
        else:
            if self.clip:
                if self.clip == len(self.index):
                    clip_offset = None
                else:
                    clip_offset = self.index[self.clip]
                self.index = self.index[:self.clip]
            else:
                clip_offset = None
            if self.shard is None and self.random_start:
                assert self.index is not None
                offset = np.random.choice(self.index)
                self.iterator = self.read_records(offset, clip_offset)
                self.iterator = itertools.chain(
                    self.iterator,
                    self.read_records(0, offset)
                )
            elif self.shard is None:
                self.iterator = self.read_records(0, clip_offset)
            else:
                shard_idx, shard_count = self.shard
                all_shard_indices = np.array_split(self.index, shard_count)
                if shard_count >= self.index.shape[0]:  # type: ignore
                    if shard_idx == 0:
                        start_byte = all_shard_indices[shard_idx][0]
                        self.iterator = self.read_records(start_byte, clip_offset)
                    else:
                        self.iterator = iter([])
                elif shard_idx < (shard_count - 1):
                    end_byte = all_shard_indices[shard_idx + 1][0]
                else:
                    end_byte = clip_offset
                start_byte = all_shard_indices[shard_idx][0]
                self.iterator = self.read_records(start_byte, end_byte)
        return self

    async def __anext__(self):
        """Asynchronous iteration to get the next record."""
        if self.iterator is None:
            raise StopAsyncIteration
        try:
            return await self.iterator.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration


    async def close(self):
        await self.file.close()

    async def process(self, record):
        return record