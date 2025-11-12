from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from app.settings import settings


def create_sync_engine() -> Engine:
    return create_engine(settings.database_url, echo=True)


def get_session() -> Generator[Session, Any]:
    engine = create_sync_engine()

    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
