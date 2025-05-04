from typing import Literal

from pydantic import BaseModel, JsonValue

from app.schema.chat_message import ChatMessageIn, MessageSeen
from app.schema.group import GroupIn


class Notification(BaseModel):
    type: Literal["error", "auth_success", "message_seen"]
    detail: JsonValue | None = None


class AuthMessage(BaseModel):
    email: str
    password: str


class MessageProtocolContainer(BaseModel):
    message: AuthMessage | ChatMessageIn | GroupIn | MessageSeen
