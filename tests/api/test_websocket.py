import asyncio
import json
from contextlib import suppress
from functools import partial

import websockets
from websockets.exceptions import ConnectionClosed

from app.db.models.users import UsersModel
from app.schema.messaging import AuthMessage, Notification


async def connect_websocket(app_url: str, data_to_send: str) -> str:
    app_answer = '{"type": "error"}'

    async with websockets.connect(app_url) as web_socket:
        message_future = asyncio.gather(web_socket.recv(decode=True))
        await asyncio.sleep(0)
        await web_socket.send(data_to_send)
        with suppress(ConnectionClosed):
            app_answer = (await message_future)[0]

    return app_answer


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
