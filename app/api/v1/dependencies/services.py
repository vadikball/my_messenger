from functools import cache
from typing import Annotated

from fastapi import Depends

from app.api.v1.dependencies.logger import LoggerDependencyType
from app.api.v1.dependencies.repos import (
    ChatsRepoDependencyType,
    GroupsRepoDependencyType,
    MessagesRepoDependencyType,
    UsersRepoDependencyType,
)
from app.containers.messaging_exception_handlers import exc_handlers
from app.services.auth import AuthService
from app.services.group import GroupsService
from app.services.history import HistoryService
from app.services.messaging import MessagingService
from app.services.password_hashing import PasswordHashingService


def get_history_service(repo: MessagesRepoDependencyType) -> HistoryService:
    return HistoryService(repo)


HistoryServiceDependencyType = Annotated[HistoryService, Depends(get_history_service)]


@cache
def get_hashing_password_service() -> PasswordHashingService:
    return PasswordHashingService()


PasswordHashingServiceDependencyType = Annotated[PasswordHashingService, Depends(get_hashing_password_service)]


def get_auth_service(
    hashing_service: PasswordHashingServiceDependencyType, repo: UsersRepoDependencyType
) -> AuthService:
    return AuthService(hashing_service, repo)


AuthServiceDependencyType = Annotated[AuthService, Depends(get_auth_service)]


@cache
def get_messaging_service(logger: LoggerDependencyType) -> MessagingService:
    return MessagingService(logger, exc_handlers)


MessagingServiceDependencyType = Annotated[MessagingService, Depends(get_messaging_service)]


def get_group_service(chats_repo: ChatsRepoDependencyType, groups_repo: GroupsRepoDependencyType) -> GroupsService:
    return GroupsService(chats_repo, groups_repo)


GroupsServiceDependencyType = Annotated[GroupsService, Depends(get_group_service)]
