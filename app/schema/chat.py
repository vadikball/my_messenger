from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from app.schema.base import BaseFromAttrs


class ChatTypeEnum(Enum):
    PERSONAL = 0
    GROUP = 1


class ChatIn(BaseModel):
    users: list[UUID]
    type: ChatTypeEnum
    name: str


class ChatMember(BaseFromAttrs):
    user_id: UUID
    chat_id: UUID


class ChatOut(BaseFromAttrs):
    id: UUID
    type: ChatTypeEnum
    name: str
    chat_members: list[ChatMember]
