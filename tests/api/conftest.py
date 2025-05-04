from datetime import UTC
from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
from faker.proxy import Faker
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chats import ChatMembersModel, ChatsModel
from app.db.models.groups import GroupsModel
from app.db.models.messages import MessagesModel
from app.db.models.users import UsersModel
from app.db.session import build_db_session_factory
from app.schema.chat_message import ChatMessageHistoryOut
from tests.types import GroupLoaderType, MessageLoaderType


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = await build_db_session_factory()
    async with session_maker() as session:
        await session.execute(delete(UsersModel))
        await session.execute(delete(ChatsModel))
        await session.commit()
        yield session


@pytest.fixture
async def users_data(faker: Faker, db_session: AsyncSession) -> list[UsersModel]:
    test_users = [
        UsersModel(
            name=faker.name(),
            email=faker.email(True, "some.domain"),
            password=faker.password(20),
        )
        for _ in range(4)
    ]
    async with db_session.begin():
        db_session.add_all(test_users)

    return test_users


@pytest.fixture
async def chats_data(faker: Faker, db_session: AsyncSession, users_data: list[UsersModel]) -> list[ChatsModel]:
    test_chats = [
        ChatsModel(
            id=uuid4(),
            name=faker.name(),
            type=0,
        )
        for _ in range(2)
    ]
    test_members = [
        ChatMembersModel(
            user_id=users_data[index % 4].id,
            chat_id=test_chats[index % 2].id,
        )
        for index in range(4)
    ]

    async with db_session.begin():
        db_session.add_all(test_chats)
        await db_session.flush()
        db_session.add_all(test_members)

    return test_chats


@pytest.fixture
async def history_data(
    faker: Faker, db_session: AsyncSession, users_data: list[UsersModel], chats_data: list[ChatsModel]
) -> list[ChatMessageHistoryOut]:
    test_messages = [
        MessagesModel(
            text=faker.text(200),
            seen=bool(index % 2),
            timestamp=faker.date_time_this_month(tzinfo=UTC),
            chat=chats_data[index % 2],
            sender=users_data[index % 4],
        )
        for index in range(19)
    ]

    async with db_session.begin():
        db_session.add_all(test_messages)

    return [ChatMessageHistoryOut.model_validate(message) for message in test_messages]


@pytest.fixture
def message_loader(db_session: AsyncSession) -> MessageLoaderType:
    async def loader(message_id: UUID) -> MessagesModel | None:  # noqa: WPS430
        return await db_session.scalar(select(MessagesModel).where(MessagesModel.id == message_id))

    return loader


@pytest.fixture
def group_loader(db_session: AsyncSession) -> GroupLoaderType:
    async def loader(group_id: UUID) -> GroupsModel | None:  # noqa: WPS430
        return await db_session.scalar(select(GroupsModel).where(GroupsModel.id == group_id))

    return loader
