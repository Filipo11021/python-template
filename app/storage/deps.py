import os
from typing import Annotated

from fastapi import Depends

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


class MyStorage(
    FileSystemStorageReadable, FileSystemStorageWritable, FileSystemStorageDeletable
):
    pass


class MyStorageInMemory(
    InMemoryStorageReadable, InMemoryStorageWritable, InMemoryStorageDeletable
):
    pass


def get_storage() -> MyStorage:
    return MyStorage(
        os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "storage",
        )
    )


StorageDep = Annotated[MyStorage, Depends(get_storage)]
