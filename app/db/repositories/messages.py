from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.messages import MessagesModel
from app.db.repositories.abc import RepoABC
from app.schema.chat_message import ChatMessage
from app.schema.history import MessagesListParams


class MessagesRepo(RepoABC[MessagesListParams, ChatMessage, MessagesModel]):
    def __init__(self, async_session: AsyncSession):
        self._session = async_session

    async def list(self, list_params: MessagesListParams) -> list[ChatMessage]:
        stmt = (
            select(MessagesModel)
            .where(MessagesModel.chat_id == list_params.chat_id)
            .order_by(MessagesModel.timestamp.asc())
            .limit(list_params.limit)
            .offset(list_params.offset)
        )
        rows = await self._session.scalars(stmt)
        return [self.to_domain(row) for row in rows]

    def to_domain(self, row: MessagesModel) -> ChatMessage:
        return ChatMessage.model_validate(row)
