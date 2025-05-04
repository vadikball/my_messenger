import asyncio
import json
import sys
import traceback
from datetime import UTC, datetime
from functools import partial
from typing import Any
from uuid import uuid4, UUID

from faker import Faker

from app.db.models.chats import ChatsModel, ChatMembersModel
from app.db.models.groups import GroupsModel, UserGroupModel
from app.db.models.messages import MessagesModel, MessageStatusModel
from app.db.models.users import UsersModel
from app.db.session import build_db_session_factory, close_db_connections

faker = Faker()


def create_json(json_file_name: str = "fake_data.json") -> None:
    args = sys.argv
    if len(args) == 2:
        json_file_name = args[1]

    users = [
        {
            "email": faker.email(),
            "name": faker.name(),
            "password": faker.password(5),
            "id": str(uuid4()),
        } for _ in range(4)
    ]

    chats = [
        {
            "name": faker.text(10),
            "id": str(uuid4()),
            "type": index % 2,
        } for index in range(4)
    ]

    chat_members = [
        {
            "user_id": users[0]["id"],
            "chat_id": chats[0]["id"],
        },
        {
            "user_id": users[1]["id"],
            "chat_id": chats[0]["id"],
        },
        {
            "user_id": users[2]["id"],
            "chat_id": chats[1]["id"],
        },
        {
            "user_id": users[3]["id"],
            "chat_id": chats[1]["id"],
        },
        {
            "user_id": users[1]["id"],
            "chat_id": chats[1]["id"],
        },
        {
            "user_id": users[2]["id"],
            "chat_id": chats[2]["id"],
        },
        {
            "user_id": users[3]["id"],
            "chat_id": chats[2]["id"],
        },
        {
            "user_id": users[0]["id"],
            "chat_id": chats[3]["id"],
        },
        {
            "user_id": users[1]["id"],
            "chat_id": chats[3]["id"],
        },
        {
            "user_id": users[2]["id"],
            "chat_id": chats[3]["id"],
        },
        {
            "user_id": users[3]["id"],
            "chat_id": chats[3]["id"],
        },

    ]

    groups = [
        {
            "name": faker.text(10),
            "id": str(uuid4()),
            "creator_id": users[0]["id"],
            "chat_id": chats[1]["id"]
        },
        {
            "name": faker.text(10),
            "id": str(uuid4()),
            "creator_id": users[2]["id"],
            "chat_id": chats[2]["id"]
        },
    ]

    user_group = [
        {
            "user_id": users[2]["id"],
            "group_id": groups[0]["id"],
        },
        {
            "user_id": users[3]["id"],
            "group_id": groups[0]["id"],
        },
        {
            "user_id": users[1]["id"],
            "group_id": groups[0]["id"],
        },
        {
            "user_id": users[0]["id"],
            "group_id": groups[1]["id"],
        },
        {
            "user_id": users[1]["id"],
            "group_id": groups[1]["id"],
        },
        {
            "user_id": users[2]["id"],
            "group_id": groups[1]["id"],
        },
        {
            "user_id": users[3]["id"],
            "group_id": groups[1]["id"],
        },
    ]

    messages = [
        {
            "id": str(uuid4()),
            "sender_id": users[0]["id"],
            "chat_id": chats[0]["id"],
            "timestamp": str(faker.date_time_this_month(tzinfo=UTC)),
            "seen": True,
            "text": faker.text(200),
        },
        {
            "id": str(uuid4()),
            "sender_id": users[1]["id"],
            "chat_id": chats[1]["id"],
            "timestamp": str(faker.date_time_this_month(tzinfo=UTC)),
            "seen": False,
            "text": faker.text(200),
        },
    ]
    message_seen_status = [
        {
            "message_id": messages[0]["id"],
            "user_id": users[0]["id"],
        },
        {
            "message_id": messages[0]["id"],
            "user_id": users[1]["id"],
        },
        {
            "message_id": messages[1]["id"],
            "user_id": users[1]["id"],
        },
        {
            "message_id": messages[1]["id"],
            "user_id": users[2]["id"],
        },
    ]

    db_fake_data = {
        "users": users,
        "chats": chats,
        "chat_members": chat_members,
        "groups": groups,
        "user_group": user_group,
        "messages": messages,
        "message_seen_status": message_seen_status,
    }
    with open(json_file_name, "w") as json_file:
        json.dump(db_fake_data, json_file, indent=4)


def convert_id(*keys: str, entity: dict[str, Any]) -> dict[str, Any]:
    new_entity = {**entity}
    for key in keys:
        new_entity[key] = UUID(new_entity[key])
    return new_entity


def convert_date(*keys: str, entity: dict[str, Any]) -> dict[str, Any]:
    new_entity = {**entity}
    for key in keys:
        new_entity[key] = datetime.fromisoformat(new_entity[key])
    return new_entity


async def populate_db(json_file_name: str = "fake_data.json") -> None:

    with open(json_file_name) as json_file:
        db_fake_data = json.load(json_file)

    session_maker = await build_db_session_factory()

    convert_primary = partial(convert_id, "id")


    async with session_maker() as session:
        session.add_all([UsersModel(**convert_primary(entity=user)) for user in db_fake_data["users"]])
        session.add_all([ChatsModel(**convert_primary(entity=chat)) for chat in db_fake_data["chats"]])
        await session.commit()
        session.add_all([GroupsModel(**convert_primary("creator_id", entity=group)) for group in db_fake_data["groups"]])
        session.add_all([ChatMembersModel(**convert_id( "user_id", "chat_id", entity=chat_member)) for chat_member in db_fake_data["chat_members"]])
        session.add_all([MessagesModel(**convert_date("timestamp", entity=convert_primary("sender_id", entity=message))) for message in db_fake_data["messages"]])
        await session.commit()
        session.add_all([UserGroupModel(**convert_id( "user_id", "group_id", entity=user_group)) for user_group in db_fake_data["user_group"]])
        session.add_all(
            [MessageStatusModel(**convert_id( "user_id", "message_id", entity=message_seen_status)) for message_seen_status in db_fake_data["message_seen_status"]]
        )
        await session.commit()

    await close_db_connections()


def add_fake_to_db() -> None:
    args = sys.argv
    if len(args) == 2:
        return asyncio.run(populate_db(args[1]))

    return asyncio.run(populate_db())
