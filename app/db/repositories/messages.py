import asyncio
from uuid import UUID

from sqlalchemy import func, select

from app.db.models.chats import ChatMembersModel
from app.db.models.messages import MessagesModel, MessageStatusModel
from app.db.repositories.abc import RepoABC
from app.schema.chat_message import ChatMessageBase, ChatMessageHistoryOut, ChatMessageOut, MessageSeen
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

    async def create(self, message: ChatMessageBase) -> ChatMessageOut:
        message_from_db = MessagesModel(**message.model_dump())
        async with self.transaction():
            self._session.add(message_from_db)
            await self._session.flush((message_from_db,))
            await self._create_status(message_from_db.id, message_from_db.sender_id)

        return ChatMessageOut.model_validate(message_from_db)

    async def create_status(self, message: MessageSeen, user_id: UUID) -> None:
        async with self.transaction():
            await self._create_status(message_id=message.message_id, user_id=user_id)

    async def detail_for_count_statuses(self, message_id: UUID) -> ChatMessageHistoryOut | None:
        async with self.transaction():
            message: MessagesModel | None = await self._session.get(MessagesModel, message_id, with_for_update=True)
            if message is None:
                return None

            seen_status_count, participants_count = await asyncio.gather(
                self._session.scalar(
                    select(func.count(MessageStatusModel.user_id)).where(MessageStatusModel.message_id == message.id)
                ),
                self._session.scalar(
                    select(func.count(ChatMembersModel.user_id)).where(ChatMembersModel.chat_id == message.chat_id)
                ),
            )

            if seen_status_count == participants_count:
                message.seen = True
                return self.to_domain(message)

            return None

    async def _create_status(self, message_id: UUID, user_id: UUID) -> None:
        self._session.add(MessageStatusModel(message_id=message_id, user_id=user_id))
