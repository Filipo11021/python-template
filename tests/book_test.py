from httpx import AsyncClient

from app.book.schemas import BookCreateRequest, BookResponse


async def test_book_flow(client: AsyncClient) -> None:
    book_to_create = BookCreateRequest(
        title="The Hitchhiker's Guide to the Galaxy",
        description="A sci-fi comedy classic.",
    )
    response = await client.post("/api/books/", json=book_to_create.model_dump())

    assert response.status_code == 200
    created_book = BookResponse.model_validate(response.json())
    assert created_book.title == book_to_create.title
    assert created_book.description == book_to_create.description
    assert created_book.id is not None
    book_id = created_book.id

    response = await client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    retrieved_book = BookResponse.model_validate(response.json())
    assert retrieved_book == created_book

    response = await client.get("/api/books/")
    assert response.status_code == 200
    books = [BookResponse.model_validate(item) for item in response.json()]
    assert created_book in books

    response = await client.delete(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json() is None

    response = await client.get(f"/api/books/{book_id}")
    assert response.status_code == 404


async def test_get_nonexistent_book(client: AsyncClient) -> None:
    response = await client.get("/api/books/99999")
    assert response.status_code == 404


async def test_delete_nonexistent_book(client: AsyncClient) -> None:
    response = await client.delete("/api/books/99999")
    assert response.status_code == 400


async def test_upload(client: AsyncClient) -> None:
    files = {"upload": ("test.txt", b"test content", "text/plain")}
    response = await client.post("/api/books/uploads", files=files)
    assert response.status_code == 200
    file_path = response.json()

    response = await client.get(f"/api/books/uploads/{file_path}")
    assert response.status_code == 200
    assert response.content == b"test content"
