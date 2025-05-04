from uuid import UUID

from pydantic import AwareDatetime, BaseModel

from app.schema.base import BaseFromAttrs


class ChatMessageSender(BaseModel):
    id: UUID
    client_id: UUID


class ChatMessageBase(BaseModel):
    sender_id: UUID
    chat_id: UUID
    text: str
    timestamp: AwareDatetime


class ChatMessageIn(ChatMessageBase):
    client_id: UUID


class ChatMessageOut(BaseFromAttrs, ChatMessageBase):
    id: UUID


class ChatMessageHistoryOut(ChatMessageOut):
    seen: bool
