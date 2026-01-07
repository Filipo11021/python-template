import os
from io import BytesIO

from app.storage.storage import (
    FileContents,
    FilePath,
    StorageDeletable,
    StorageReadable,
    StorageWritable,
)


class FileSystemStorageWritable(StorageWritable):
    def __init__(self, directory: str) -> None:
        self.directory = directory

    async def write(self, path: FilePath, contents: FileContents) -> None:
        full_path = os.path.join(self.directory, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(contents.read())


class FileSystemStorageReadable(StorageReadable):
    def __init__(self, directory: str) -> None:
        self.directory = directory

    async def read(self, path: FilePath) -> FileContents:
        full_path = os.path.join(self.directory, path)
        with open(full_path, "rb") as f:
            return BytesIO(f.read())


class FileSystemStorageDeletable(StorageDeletable):
    def __init__(self, directory: str) -> None:
        self.directory = directory

    async def delete(self, path: FilePath) -> None:
        full_path = os.path.join(self.directory, path)
        os.remove(full_path)
