from app.storage.storage import (
    FileContents,
    FilePath,
    StorageDeletable,
    StorageReadable,
    StorageWritable,
)


class InMemoryStorageWritable(StorageWritable):
    def __init__(self, storage: dict[FilePath, FileContents]) -> None:
        self.storage = storage

    async def write(self, path: FilePath, contents: FileContents) -> None:
        self.storage[path] = contents


class InMemoryStorageReadable(StorageReadable):
    def __init__(self, storage: dict[FilePath, FileContents]) -> None:
        self.storage = storage

    async def read(self, path: FilePath) -> FileContents:
        return self.storage[path]


class InMemoryStorageDeletable(StorageDeletable):
    def __init__(self, storage: dict[FilePath, FileContents]) -> None:
        self.storage = storage

    async def delete(self, path: FilePath) -> None:
        del self.storage[path]
