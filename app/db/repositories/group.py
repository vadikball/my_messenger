from uuid import UUID

from app.db.models.groups import GroupsModel, UserGroupModel
from app.db.repositories.abc import RepoABC
from app.schema.group import GroupIn, GroupOut, UserGroup


class GroupsRepo(RepoABC[GroupsModel, GroupOut]):
    domain = GroupOut

    async def create(self, group: GroupIn, chat_id: UUID, creator_id: UUID) -> GroupOut:
        group_from_db = GroupsModel(name=group.name, chat_id=chat_id, creator_id=creator_id)

        async with self.transaction():
            self._session.add(group_from_db)
            await self._session.flush((group_from_db,))

            users_in_group = [UserGroupModel(user_id=user_id, group_id=group_from_db.id) for user_id in group.users]
            self._session.add_all(users_in_group)

        return GroupOut(
            id=group_from_db.id,
            name=group_from_db.name,
            creator_id=group_from_db.creator_id,
            chat_id=group_from_db.chat_id,
            user_group=[UserGroup.model_validate(user_group) for user_group in users_in_group],
        )
