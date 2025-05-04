from sqlalchemy import select

from app.db.models.messages import MessagesModel
from app.db.repositories.abc import RepoABC
from app.schema.chat_message import ChatMessageHistoryOut, ChatMessageIn, ChatMessageOut
from app.schema.history import MessagesListParams


class MessagesRepo(RepoABC[MessagesModel, ChatMessageHistoryOut]):
    domain = ChatMessageHistoryOut

    async def list(self, list_params: MessagesListParams) -> list[ChatMessageHistoryOut]:
        stmt = (
            select(MessagesModel)
            .where(MessagesModel.chat_id == list_params.chat_id)
            .order_by(MessagesModel.timestamp.asc())
            .limit(list_params.limit)
            .offset(list_params.offset)
        )
        rows = await self._session.scalars(stmt)
        return [self.to_domain(row) for row in rows]

    async def create(self, message: ChatMessageIn) -> ChatMessageOut:
        message_from_db = MessagesModel(**message.model_dump())
        self._session.add(message_from_db)
        await self._session.commit()
        return ChatMessageOut.model_validate(message_from_db)
