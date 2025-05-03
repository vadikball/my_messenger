from abc import abstractmethod

from app.containers.web_socket import WebSocketContainer
from app.services.abc import MessagingServiceABC
from app.type.base import MessagingHandlerType


class MessagingExceptionHandlerABC:
    @abstractmethod
    async def message_handle(
        self,
        messaging_service: MessagingServiceABC,
        message_handler: MessagingHandlerType,
        container: WebSocketContainer,
    ) -> None: ...
