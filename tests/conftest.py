from typing import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.settings import settings
from app.main import app


@pytest.fixture(scope="session")
async def app_url() -> str:
    return f"ws://{settings.APP_HOST}/ws"


@pytest.fixture
async def started_app() -> AsyncIterator[FastAPI]:
    async with LifespanManager(app) as manager:
        yield manager.app  # type: ignore


@pytest.fixture
async def app_client(started_app: FastAPI) -> AsyncIterator[AsyncClient]:

    async with AsyncClient(transport=ASGITransport(app=started_app), base_url="http://test") as client:
        yield client
