from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.v1.dependencies.services import HistoryServiceDependencyType
from app.schema.chat_message import ChatMessageHistoryOut
from app.schema.history import MessagesListBaseParams

router = APIRouter()


@router.get("/history/{chat_id}")
async def get_chat_history(
    chat_id: UUID, history_params: Annotated[MessagesListBaseParams, Query()], service: HistoryServiceDependencyType
) -> list[ChatMessageHistoryOut]:
    return await service.get_chat_history(chat_id, history_params)
