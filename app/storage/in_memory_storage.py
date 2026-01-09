from io import BytesIO

from app.storage.storage import (
    FileContents,
    FilePath,
    StorageDeletable,
    StorageReadable,
    StorageWritable,
)

type InMemoryStorageDict = dict[FilePath, bytes]


class InMemoryStorageWritable(StorageWritable):
    def __init__(self, storage: InMemoryStorageDict) -> None:
        self.storage = storage

    async def write(self, path: FilePath, contents: FileContents) -> None:
        self.storage[path] = contents.read()


class InMemoryStorageReadable(StorageReadable):
    def __init__(self, storage: InMemoryStorageDict) -> None:
        self.storage = storage

    async def read(self, path: FilePath) -> FileContents:
        return BytesIO(self.storage[path])


class InMemoryStorageDeletable(StorageDeletable):
    def __init__(self, storage: InMemoryStorageDict) -> None:
        self.storage = storage

    async def delete(self, path: FilePath) -> None:
        del self.storage[path]
