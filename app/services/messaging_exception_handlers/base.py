from pydantic import ValidationError

from app.containers.web_socket import WebSocketContainer
from app.exc.base import MessagingException
from app.schema.messaging import Notification
from app.services.abc import MessagingServiceABC
from app.services.messaging_exception_handlers.abc import MessagingExceptionHandlerABC
from app.type.base import MessagingHandlerType


class MessagingExceptionHandler(MessagingExceptionHandlerABC):
    def __init__(self, exc_type: type[MessagingException] | type[ValidationError]):
        self._exc_type = exc_type

    async def message_handle(
        self,
        messaging_service: MessagingServiceABC,
        message_handle: MessagingHandlerType,
        container: WebSocketContainer,
    ) -> None:
        try:
            await message_handle(container)
        except self._exc_type as exc:
            await self.process_exc(messaging_service, container, exc)

    async def process_exc(
        self,
        messaging_service: MessagingServiceABC,
        container: WebSocketContainer,
        exc: MessagingException | ValidationError,
    ) -> None:
        await messaging_service.send_message(Notification(type="error", detail=exc.json()), container)
