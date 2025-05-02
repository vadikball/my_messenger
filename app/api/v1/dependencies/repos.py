from typing import Annotated

from fastapi import Depends

from app.api.v1.dependencies.session import AsyncSessionDependencyType
from app.db.repositories.messages import MessagesRepo


def get_messages_repo(session: AsyncSessionDependencyType) -> MessagesRepo:
    return MessagesRepo(session)


MessagesRepoDependencyType = Annotated[MessagesRepo, Depends(get_messages_repo)]
