from collections.abc import AsyncGenerator, Generator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.settings import settings


def get_sync_connection_string() -> str:
    return f"sqlite:///{settings.db_name}"


def get_async_connection_string() -> str:
    return f"sqlite+aiosqlite:///{settings.db_name}"


def create_sync_database_engine() -> Engine:
    return create_engine(get_sync_connection_string(), echo=True)


def get_session() -> Generator[Session, Any]:
    engine = create_sync_database_engine()

    with Session(engine) as session:
        yield session


async def create_async_database_engine() -> AsyncEngine:
    return create_async_engine(get_async_connection_string(), echo=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    engine = await create_async_database_engine()

    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
