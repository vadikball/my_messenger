import asyncio
import json
from contextlib import suppress
from datetime import UTC, datetime
from functools import partial
from uuid import uuid4

import websockets

from app.db.models.chats import ChatsModel
from app.db.models.users import UsersModel
from app.schema.chat_message import ChatMessageIn, ChatMessageOut, ChatMessageSender
from app.schema.group import GroupIn, GroupOut
from app.schema.messaging import AuthMessage, Notification
from tests.types import GroupLoaderType, MessageLoaderType


async def wait_message(client: websockets.ClientConnection, barrier: asyncio.Barrier) -> str:
    app_answer = '{"type": "error"}'

    message_future = asyncio.gather(client.recv(decode=True))
    await barrier.wait()
    with suppress(websockets.ConnectionClosed):
        app_answer = (await message_future)[0]

    return app_answer


async def send_message(client: websockets.ClientConnection, data_to_send: str, barrier: asyncio.Barrier) -> None:
    await barrier.wait()
    await client.send(data_to_send)


async def connect_websocket(app_url: str, data_to_send: str) -> str:
    async with websockets.connect(app_url) as web_socket:
        barrier = asyncio.Barrier(2)
        futures = asyncio.gather(wait_message(web_socket, barrier), send_message(web_socket, data_to_send, barrier))
        return (await futures)[0]


async def imitate_chat(app_url: str, auth_message: str, chat_message: str | None, chat_barrier: asyncio.Barrier) -> str:
    async with websockets.connect(app_url) as web_socket:
        barrier = asyncio.Barrier(2)
        futures = asyncio.gather(wait_message(web_socket, barrier), send_message(web_socket, auth_message, barrier))
        await futures

        wait_future = asyncio.gather(wait_message(web_socket, chat_barrier))
        if chat_message is not None:
            await send_message(web_socket, chat_message, chat_barrier)

        return (await asyncio.wait_for(wait_future, 0.5))[0]


async def test_websocket(users_data: list[UsersModel], app_url: str) -> None:
    messages = (
        AuthMessage(email=users_data[0].email, password=users_data[0].password),
        AuthMessage(email=users_data[1].email, password=users_data[1].password),
        '{ "any": "Any string" }',
        AuthMessage(email=users_data[2].email, password=users_data[2].email),
    )
    connect_ws = partial(connect_websocket, app_url)

    futures = asyncio.gather(
        connect_ws(messages[0].model_dump_json()),
        connect_ws(messages[1].model_dump_json()),
        connect_ws(messages[2]),
        connect_ws(messages[3].model_dump_json()),
    )

    result_messages = tuple(map(json.loads, await futures))

    assert Notification.model_validate_json(result_messages[0]) == Notification(type="auth_success")
    assert Notification.model_validate_json(result_messages[1]) == Notification(type="auth_success")
    assert Notification.model_validate_json(result_messages[3]) == Notification(
        type="error", detail='{"detail": "user not authenticated"}'
    )

    validation_notification = Notification.model_validate_json(result_messages[2])
    assert validation_notification.type == "error"
    assert validation_notification.detail is not None


def create_auth_message_dump(user: UsersModel) -> str:
    return AuthMessage(email=user.email, password=user.password).model_dump_json()


async def test_messages(
    users_data: list[UsersModel], chats_data: list[ChatsModel], app_url: str, message_loader: MessageLoaderType
) -> None:

    auth_messages = tuple(create_auth_message_dump(user) for user in users_data)
    chat_messages = (
        ChatMessageIn(
            client_id=uuid4(),
            sender_id=users_data[0].id,
            chat_id=chats_data[0].id,
            timestamp=datetime.now(tz=UTC),
            text=users_data[2].name,
        ),
        ChatMessageIn(
            client_id=uuid4(),
            sender_id=users_data[1].id,
            chat_id=chats_data[1].id,
            timestamp=datetime.now(tz=UTC),
            text=users_data[3].name,
        ),
    )
    chat_messages_json = tuple(chat_message.model_dump_json() for chat_message in chat_messages)

    barriers = (asyncio.Barrier(3), asyncio.Barrier(3))
    futures = asyncio.gather(
        imitate_chat(app_url, auth_messages[0], chat_messages_json[0], barriers[0]),
        imitate_chat(app_url, auth_messages[1], chat_messages_json[1], barriers[1]),
        imitate_chat(app_url, auth_messages[2], None, barriers[0]),
        imitate_chat(app_url, auth_messages[3], None, barriers[1]),
    )

    future_results = await futures

    success = (
        ChatMessageOut.model_validate_json(json.loads(future_results[2])),
        ChatMessageOut.model_validate_json(json.loads(future_results[3])),
    )

    first_client_id = ChatMessageSender.model_validate_json(json.loads(future_results[0])).client_id
    second_client_id = ChatMessageSender.model_validate_json(json.loads(future_results[1])).client_id

    assert success[0].text == users_data[2].name
    assert chat_messages[0].client_id == first_client_id
    assert success[1].text == users_data[3].name
    assert chat_messages[1].client_id == second_client_id

    messages_in_db = await asyncio.gather(message_loader(success[0].id), message_loader(success[1].id))

    assert messages_in_db[0] and messages_in_db[1]


async def test_new_group(users_data: list[UsersModel], app_url: str, group_loader: GroupLoaderType) -> None:
    auth_messages = tuple(create_auth_message_dump(user) for user in users_data[:2])

    group_message = GroupIn(name="test chat", users=[user.id for user in users_data]).model_dump_json()

    barrier = asyncio.Barrier(3)

    futures = asyncio.gather(
        imitate_chat(app_url, auth_messages[0], group_message, barrier),
        imitate_chat(app_url, auth_messages[1], None, barrier),
        connect_websocket(app_url, group_message),
    )

    future_results = await futures

    group = GroupOut.model_validate_json(json.loads(future_results[0]))

    assert GroupOut.model_validate_json(json.loads(future_results[1]))
    assert Notification.model_validate_json(json.loads(future_results[2])) == Notification(
        type="error", detail='{"detail": "access denied"}'
    )

    assert await group_loader(group.id)
