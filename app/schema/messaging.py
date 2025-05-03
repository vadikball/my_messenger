from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, JsonValue


class Notification(BaseModel):
    type: Literal["error", "auth_success", "message_seen"]
    detail: JsonValue | None = None


class AuthMessage(BaseModel):
    email: str
    password: str


class ChatMessageIn(BaseModel):
    sender_id: UUID
    chat_id: UUID
    text: str
    timestamp: datetime


class MessageProtocolContainer(BaseModel):
    message: AuthMessage | ChatMessageIn
