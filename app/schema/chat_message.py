from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChatMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sender_id: UUID
    chat_id: UUID
    text: str
    seen: bool
    timestamp: datetime
