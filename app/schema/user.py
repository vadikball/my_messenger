from uuid import UUID

from app.schema.base import BaseFromAttrs


class UserSchema(BaseFromAttrs):
    id: UUID
    name: str
    email: str
    password: str
