from typing import AsyncIterator
from uuid import UUID

from sqlalchemy import select

from app.db.models.chats import ChatMembersModel, ChatsModel
from app.db.repositories.abc import RepoABC
from app.schema.chat import ChatIn, ChatMember, ChatOut


class ChatsRepo(RepoABC[ChatsModel, ChatOut]):
    domain = ChatOut

    async def create(self, chat: ChatIn) -> ChatOut:
        chat_from_db = ChatsModel(
            name=chat.name,
            type=chat.type.value,
        )
        self._session.add(chat_from_db)
        await self._session.flush((chat_from_db,))
        chat_members = [ChatMembersModel(user_id=user_id, chat_id=chat_from_db.id) for user_id in chat.users]
        self._session.add_all(chat_members)

        await self._session.commit()
        return ChatOut(
            id=chat_from_db.id,
            name=chat.name,
            type=chat.type,
            chat_members=[ChatMember.model_validate(member) for member in chat_members],
        )


class ChatMembersRepo(RepoABC[ChatMembersModel, ChatMember]):
    domain = ChatMember

    async def get_members(self, chat_id: UUID) -> AsyncIterator[ChatMember]:
        stmt = select(ChatMembersModel).where(ChatMembersModel.chat_id == chat_id)
        members_stream = await self._session.stream(stmt)

        async for member_from_db in members_stream.scalars():
            yield self.to_domain(member_from_db)
