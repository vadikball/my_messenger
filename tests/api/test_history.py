from datetime import datetime

from httpx import AsyncClient

from app.schema.chat_message import ChatMessage


def message_sort(message: ChatMessage) -> datetime:
    return message.timestamp


async def test_history(app_client: AsyncClient, history_data: list[ChatMessage]) -> None:
    sorted_history = sorted(history_data[::2], key=message_sort)
    first_chat_messages = [message.model_dump(mode="json") for message in sorted_history]

    default_params = {"limit": 10, "offset": 0}
    response = await app_client.get(f"/history/{history_data[0].chat_id}", params=default_params)

    assert response.json() == first_chat_messages

    response = await app_client.get(f"/history/{history_data[1].chat_id}", params=default_params)

    assert len(response.json()) == 9

    response = await app_client.get("/history/str", params={"limit": 0, "offset": -1})

    unprocessable_entity_error_json = {
        "detail": [
            {
                "type": "uuid_parsing",
                "loc": ["path", "chat_id"],
                "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of "
                "`urn:uuid:` followed by [0-9a-fA-F-], found `s` at 1",
                "input": "str",
                "ctx": {
                    "error": "invalid character: expected an optional prefix of "
                    "`urn:uuid:` followed by [0-9a-fA-F-], found `s` at 1"
                },
            },
            {
                "type": "greater_than",
                "loc": ["query", "limit"],
                "msg": "Input should be greater than 0",
                "input": "0",
                "ctx": {"gt": 0},
            },
            {
                "type": "greater_than_equal",
                "loc": ["query", "offset"],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1",
                "ctx": {"ge": 0},
            },
        ]
    }

    assert response.json() == unprocessable_entity_error_json
