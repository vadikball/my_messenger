from fastapi import APIRouter

from app.api.v1.dependencies.container import WebSocketContainerDependencyType
from app.api.v1.dependencies.services import MessagingServiceDependencyType

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    container: WebSocketContainerDependencyType, messaging_service: MessagingServiceDependencyType
) -> None:
    await messaging_service.connect(container)
    await messaging_service.keep(container)
