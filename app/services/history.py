from uuid import UUID

from app.db.repositories.messages import MessagesRepo
from app.schema.chat_message import ChatMessage
from app.schema.history import MessagesListBaseParams, MessagesListParams


class HistoryService:
    def __init__(self, message_repo: MessagesRepo):
        self._repo = message_repo

    async def get_chat_history(self, chat_id: UUID, history_params: MessagesListBaseParams) -> list[ChatMessage]:
        return await self._repo.list(
            list_params=MessagesListParams(
                chat_id=chat_id,
                limit=history_params.limit,
                offset=history_params.offset,
            )
        )
