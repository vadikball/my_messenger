from datetime import datetime
from uuid import UUID

from app.schema.base import BaseFromAttrs


class ChatMessage(BaseFromAttrs):

    id: UUID
    sender_id: UUID
    chat_id: UUID
    text: str
    seen: bool
    timestamp: datetime
