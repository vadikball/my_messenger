"""Application with configuration for events, routers and middleware."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.dependencies.logger import get_logger
from app.api.v1.dependencies.services import get_messaging_service
from app.api.v1.history import router as history_router
from app.api.v1.websocket import router as websocket_router
from app.core.settings import settings
from app.db import session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await session.verify_db_connection(session.engine)
    session.session_factory_cache = await session.build_db_session_factory()
    yield
    await get_messaging_service(get_logger()).shutdown()
    await session.close_db_connections()


def get_application() -> FastAPI:
    """Create configured server application instance."""

    application = FastAPI(
        debug=settings.DEBUG,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        docs_url="/docs" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(history_router)
    application.include_router(websocket_router)

    return application


app = get_application()
