from asyncio import Lock
from typing import Annotated, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies.session import AsyncSessionDependencyType
from app.db.repositories.abc import RepoABC
from app.db.repositories.chats import ChatMembersRepo, ChatsRepo
from app.db.repositories.group import GroupsRepo
from app.db.repositories.messages import MessagesRepo
from app.db.repositories.users import UsersRepo


def repo_deps_factory[RepoType: RepoABC](
    repo_type: type[RepoType], deps_name: str
) -> Callable[[tuple[AsyncSession, Lock]], RepoType]:

    def new_repo_deps(session_lock: AsyncSessionDependencyType) -> RepoType:  # noqa: WPS430
        session, lock = session_lock
        return repo_type(session, lock)

    new_repo_deps.__name__ = deps_name

    return new_repo_deps


get_messages_repo = repo_deps_factory(MessagesRepo, "get_messages_repo")
MessagesRepoDependencyType = Annotated[MessagesRepo, Depends(get_messages_repo)]

get_users_repo = repo_deps_factory(UsersRepo, "get_users_repo")
UsersRepoDependencyType = Annotated[UsersRepo, Depends(get_users_repo)]

get_chat_members_repo = repo_deps_factory(ChatMembersRepo, "get_chat_members_repo")
ChatMembersRepoDependencyType = Annotated[ChatMembersRepo, Depends(get_chat_members_repo)]

get_chats_repo = repo_deps_factory(ChatsRepo, "get_chats_repo")
ChatsRepoDependencyType = Annotated[ChatsRepo, Depends(get_chats_repo)]

get_groups_repo = repo_deps_factory(GroupsRepo, "get_groups_repo")
GroupsRepoDependencyType = Annotated[GroupsRepo, Depends(get_groups_repo)]
