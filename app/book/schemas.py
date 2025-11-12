from collections.abc import Sequence

from pydantic import BaseModel

from app.book.models import Book


class BookCreateRequest(BaseModel):
    title: str
    description: str


class BookResponse(BaseModel):
    id: int
    title: str
    description: str


def book_to_response(book: Book) -> BookResponse:
    if book.id is None:
        raise ValueError("Book ID is missing")

    return BookResponse(
        id=book.id,
        title=book.title,
        description=book.description,
    )


def books_to_response(books: Sequence[Book]) -> list[BookResponse]:
    return [book_to_response(book) for book in books]
