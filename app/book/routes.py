from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.book.models import Book
from app.book.schemas import (
    BookCreateRequest,
    BookResponse,
    book_to_response,
    books_to_response,
)
from app.database import AsyncSessionDep, SessionDep

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    "/",
)
async def get_books(session: SessionDep) -> list[BookResponse]:
    books = session.exec(select(Book)).all()

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
