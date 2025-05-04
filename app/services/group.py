from uuid import UUID

from app.db.repositories.chats import ChatsRepo
from app.db.repositories.group import GroupsRepo
from app.schema.chat import ChatIn, ChatTypeEnum
from app.schema.group import GroupIn, GroupOut


class GroupsService:
    def __init__(self, chat_repo: ChatsRepo, group_repo: GroupsRepo):
        self._group_repo = group_repo
        self._chat_repo = chat_repo

    async def create_group(self, group: GroupIn, creator_id: UUID) -> GroupOut:
        new_chat = ChatIn(users=group.users, type=ChatTypeEnum.GROUP, name=group.name)
        created_chat = await self._chat_repo.create(new_chat)
        return await self._group_repo.create(group, created_chat.id, creator_id)
