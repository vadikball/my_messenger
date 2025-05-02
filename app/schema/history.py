from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class MessagesListBaseParams(BaseModel):
    limit: PositiveInt
    offset: NonNegativeInt


class MessagesListParams(BaseModel):
    chat_id: UUID
    limit: PositiveInt
    offset: NonNegativeInt
