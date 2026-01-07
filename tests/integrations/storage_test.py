import shutil
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

import pytest

from app.storage.file_system_storage import (
    FileSystemStorageDeletable,
    FileSystemStorageReadable,
    FileSystemStorageWritable,
)
from app.storage.in_memory_storage import (
    InMemoryStorageDeletable,
    InMemoryStorageReadable,
    InMemoryStorageWritable,
)


def remove_directory(path: str | Path) -> None:
    directory = Path(path)
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory)


async def test_in_memory_storage() -> None:
    storage: dict[str, BinaryIO] = {}

    writable = InMemoryStorageWritable(storage)
    readable = InMemoryStorageReadable(storage)
    deletable = InMemoryStorageDeletable(storage)

    path = "test"
    contents = b"aaaaa"

    await writable.write(path, BytesIO(contents))

    read_contents = await readable.read(path)

    assert read_contents.read() == contents

    await deletable.delete(path)

    with pytest.raises(Exception):
        await readable.read(path)


async def test_in_file_system_storage() -> None:
    storage: str = "tmp_test_storage"

    try:
        writable = FileSystemStorageWritable(storage)
        readable = FileSystemStorageReadable(storage)
        deletable = FileSystemStorageDeletable(storage)

        path = "test"
        contents = b"aaaaa"

        await writable.write(path, BytesIO(contents))

        read_contents = await readable.read(path)

        assert read_contents.read() == contents

        await deletable.delete(path)

        with pytest.raises(Exception):
            await readable.read(path)
    finally:
        remove_directory(storage)
