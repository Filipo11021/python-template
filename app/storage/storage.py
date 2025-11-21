from abc import ABC, abstractmethod

FileContents = bytes
FilePath = str


class StorageWritable(ABC):
    @abstractmethod
    async def write(self, path: FilePath, contents: FileContents) -> None:
        raise NotImplementedError


class StorageReadable(ABC):
    @abstractmethod
    async def read(self, path: FilePath) -> FileContents:
        raise NotImplementedError


class StorageDeletable(ABC):
    @abstractmethod
    async def delete(self, path: FilePath) -> None:
        raise NotImplementedError
