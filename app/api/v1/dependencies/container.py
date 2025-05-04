from typing import Annotated

from fastapi import Depends, WebSocket

from app.api.v1.dependencies.repos import ChatMembersRepoDependencyType, MessagesRepoDependencyType
from app.api.v1.dependencies.services import AuthServiceDependencyType
from app.containers.web_socket import WebSocketContainer


def get_websocket_container(
    websocket: WebSocket,
    auth_service: AuthServiceDependencyType,
    messages_repo: MessagesRepoDependencyType,
    chat_members_repo: ChatMembersRepoDependencyType,
) -> WebSocketContainer:
    return WebSocketContainer(auth_service, messages_repo, chat_members_repo, websocket)


WebSocketContainerDependencyType = Annotated[WebSocketContainer, Depends(get_websocket_container)]
