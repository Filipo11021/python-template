from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel, create_engine

from app.create_app import create_app
from app.database import get_session

sqlite_file_name = ":memory:"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def test_create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def reset_database() -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def test_get_session() -> Generator[Session, Any]:
    with Session(engine) as session:
        yield session


def override_get_session(app: FastAPI) -> None:
    app.dependency_overrides[get_session] = test_get_session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    print("creating database")  # noqa: T201
    test_create_db_and_tables()
    print("database created")  # noqa: T201
    yield
    print("resetting database")  # noqa: T201
    reset_database()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient]:
    app = create_app(lifespan=lifespan)

    override_get_session(app)

    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app),
            base_url="http://localhost",
            follow_redirects=True,
        ) as client:
            yield client
