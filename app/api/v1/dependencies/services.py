from typing import Annotated

from fastapi import Depends

from app.api.v1.dependencies.repos import MessagesRepoDependencyType
from app.services.history import HistoryService


def get_history_service(repo: MessagesRepoDependencyType) -> HistoryService:
    return HistoryService(repo)


HistoryServiceDependencyType = Annotated[HistoryService, Depends(get_history_service)]
