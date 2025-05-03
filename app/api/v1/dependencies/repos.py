from typing import Annotated

from fastapi import Depends

from app.api.v1.dependencies.session import AsyncSessionDependencyType
from app.db.repositories.messages import MessagesRepo
from app.db.repositories.users import UsersRepo


def get_messages_repo(session: AsyncSessionDependencyType) -> MessagesRepo:
    return MessagesRepo(session)


MessagesRepoDependencyType = Annotated[MessagesRepo, Depends(get_messages_repo)]


def get_users_repo(session: AsyncSessionDependencyType) -> UsersRepo:
    return UsersRepo(session)


UsersRepoDependencyType = Annotated[UsersRepo, Depends(get_users_repo)]
