from uuid import UUID

from app.schema.base import BaseFromAttrs


class UserGroup(BaseFromAttrs):
    user_id: UUID
    group_id: UUID


class GroupBase(BaseFromAttrs):
    name: str


class GroupIn(GroupBase):
    users: list[UUID]


class GroupOut(GroupBase):
    id: UUID
    chat_id: UUID
    creator_id: UUID
    user_group: list[UserGroup]
