import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Response, UploadFile
from sqlmodel import select

from app.background_runner.deps import BackgroundRunnerDep
from app.book.models import Book
from app.book.schemas import (
    BookCreateRequest,
    BookResponse,
    book_to_response,
    books_to_response,
)
from app.database import AsyncSessionDep
from app.logger import LoggerDep
from app.mailer import MailerDep, MailMessage
from app.storage.deps import StorageDep

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    "/",
)
async def get_books(session: AsyncSessionDep) -> list[BookResponse]:
    result = await session.exec(select(Book))
    books = result.all()

    return books_to_response(books)


@router.get("/{book_id}")
async def get_book(book_id: int, session: AsyncSessionDep) -> BookResponse:
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book_to_response(book)


@router.post("/")
async def create_book(
    data: BookCreateRequest, session: AsyncSessionDep
) -> BookResponse:
    book = Book(description=data.description, title=data.title)
    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book_to_response(book)


@router.delete("/{book_id}", response_model=type(None))
async def delete_book(book_id: int, session: AsyncSessionDep) -> None:
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=400, detail="Invalid book ID")

    await session.delete(book)
    await session.commit()

    return None


@router.post("/notify")
async def notify(mailer: MailerDep) -> None:
    await mailer.send(MailMessage(to="test@example.com", subject="Test", body="Test"))
    return None


@router.post("/uploads")
async def upload_file(upload: UploadFile, storage: StorageDep) -> str:
    file_path = upload.filename or uuid4().hex

    await storage.write(file_path, upload.file)

    return file_path


@router.get("/uploads/{file_path}")
async def get_upload(file_path: str, storage: StorageDep) -> Response:
    return Response(
        content=await storage.read(file_path), media_type="application/octet-stream"
    )


def heavy_task(logger: LoggerDep) -> None:
    logger.info("Heavy task started")
    time.sleep(10)
    logger.info("Heavy task completed")


@router.post("/background-tasks")
async def background_tasks(
    background_runner: BackgroundRunnerDep, logger: LoggerDep
) -> None:
    await background_runner.add_task(heavy_task, logger=logger)

    return None
