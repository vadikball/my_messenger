from typing import AsyncIterator
from uuid import UUID

from sqlalchemy import select

from app.db.models.chats import ChatMembersModel
from app.db.repositories.abc import RepoABC
from app.schema.chat import ChatMember


class ChatMembersRepo(RepoABC[ChatMembersModel, ChatMember]):
    domain = ChatMember

    async def get_members(self, chat_id: UUID) -> AsyncIterator[ChatMember]:
        stmt = select(ChatMembersModel).where(ChatMembersModel.chat_id == chat_id)
        members_stream = await self._session.stream(stmt)

        async for member_from_db in members_stream.scalars():
            yield self.to_domain(member_from_db)
