from uuid import UUID

from app.schema.base import BaseFromAttrs


class ChatMember(BaseFromAttrs):
    user_id: UUID
    chat_id: UUID
