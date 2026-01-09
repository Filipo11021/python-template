from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.create_app import create_app
from app.database import get_async_session
from app.storage.deps import MyStorageInMemory, get_storage
from app.storage.in_memory_storage import InMemoryStorageDict

sqlite_file_name = ":memory:"
async_sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"


async def create_in_memory_async_engine() -> AsyncEngine:
    return create_async_engine(
        async_sqlite_url, echo=True, connect_args={"check_same_thread": False}
    )


engine = None


async def test_create_db_and_tables() -> None:
    global engine
    engine = await create_in_memory_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def reset_database() -> None:
    global engine
    if engine:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)


async def test_get_session() -> AsyncGenerator[AsyncSession, Any]:
    global engine
    if not engine:
        engine = await create_in_memory_async_engine()
    async with AsyncSession(engine) as session:
        yield session


def create_override_get_storage(
    storage: InMemoryStorageDict,
) -> Callable[[], MyStorageInMemory]:
    return lambda: MyStorageInMemory(storage)


def override_get_session(app: FastAPI) -> None:
    app.dependency_overrides[get_async_session] = test_get_session


def override_get_storage(app: FastAPI, storage: InMemoryStorageDict) -> None:
    app.dependency_overrides[get_storage] = create_override_get_storage(storage)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    global engine
    await test_create_db_and_tables()
    yield
    await reset_database()
    if engine:
        await engine.dispose()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient]:
    app = create_app(lifespan=lifespan)

    override_get_session(app)
    override_get_storage(app, {})

    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app),
            base_url="http://localhost",
            follow_redirects=True,
        ) as client:
            yield client
