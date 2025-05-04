from uuid import UUID

from pydantic import AwareDatetime

from app.schema.base import BaseFromAttrs


class ChatMessageIn(BaseFromAttrs):
    sender_id: UUID
    chat_id: UUID
    text: str
    timestamp: AwareDatetime


class ChatMessageOut(ChatMessageIn):
    id: UUID


class ChatMessageHistoryOut(ChatMessageOut):
    seen: bool
