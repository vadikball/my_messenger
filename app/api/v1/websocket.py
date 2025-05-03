from fastapi import APIRouter, WebSocket

from app.api.v1.dependencies.services import AuthServiceDependencyType, MessagingServiceDependencyType

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, messaging_service: MessagingServiceDependencyType, auth_service: AuthServiceDependencyType
) -> None:
    container = await messaging_service.connect(websocket, auth_service)
    await messaging_service.keep(container)
