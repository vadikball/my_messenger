from datetime import UTC
from typing import AsyncGenerator, AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from faker.proxy import Faker
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chats import ChatsModel
from app.db.models.messages import MessagesModel
from app.db.models.users import UsersModel
from app.db.session import build_db_session_factory
from app.main import app
from app.schema.chat_message import ChatMessage

# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture
async def started_app() -> AsyncIterator[FastAPI]:
    async with LifespanManager(app) as manager:
        yield manager.app  # type: ignore


@pytest.fixture
async def app_client(started_app: FastAPI) -> AsyncIterator[AsyncClient]:

    async with AsyncClient(transport=ASGITransport(app=started_app), base_url="http://test") as client:
        yield client


# @pytest.fixture(scope="session")
# async def apply_migration() -> AsyncSession:
#     ...


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = await build_db_session_factory()
    async with session_maker() as session:
        await session.execute(delete(UsersModel))
        await session.execute(delete(ChatsModel))
        await session.commit()
        yield session


@pytest.fixture
async def history_data(faker: Faker, db_session: AsyncSession) -> list[ChatMessage]:
    test_users = [
        UsersModel(
            name=faker.name(),
            email=faker.email(True, "some.domain"),
            password=faker.password(20),
        )
        for _ in range(4)
    ]
    test_chats = [
        ChatsModel(
            name=faker.name(),
            type=0,
        )
        for _ in range(2)
    ]
    test_messages = [
        MessagesModel(
            text=faker.text(200),
            seen=bool(index % 2),
            timestamp=faker.date_time_this_month(tzinfo=UTC),
            chat=test_chats[index % 2],
            sender=test_users[index % 4],
        )
        for index in range(19)
    ]

    async with db_session.begin():
        db_session.add_all([*test_users, *test_chats, *test_messages])

    return [ChatMessage.model_validate(message) for message in test_messages]
