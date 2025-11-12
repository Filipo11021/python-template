from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import Lifespan

from app.book import routes as book_routes
from app.settings import settings


def create_app(lifespan: Lifespan[FastAPI] | None = None) -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_router = APIRouter(prefix="/api")

    api_router.include_router(book_routes.router)

    app.include_router(api_router)

    return app
