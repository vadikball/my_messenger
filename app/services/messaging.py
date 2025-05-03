import asyncio
from functools import partial
from typing import TYPE_CHECKING, Any
from uuid import UUID
from weakref import WeakSet

from fastapi import WebSocket
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect, WebSocketState

from app.containers.web_socket import WebSocketContainer
from app.core.logger import LoggerBase
from app.schema.messaging import AuthMessage, MessageProtocolContainer, Notification
from app.services.abc import MessagingServiceABC
from app.services.auth import AuthService
from app.services.messaging_exception_handlers.abc import MessagingExceptionHandlerABC

if TYPE_CHECKING:
    from loguru import Logger


class MessagingService(MessagingServiceABC, LoggerBase):
    _user_connections: dict[UUID, WebSocketContainer]
    _events: WeakSet[asyncio.Event]
    _futures: WeakSet[asyncio.Future]

    def __init__(self, simple_logger: "Logger", exc_handlers: tuple[MessagingExceptionHandlerABC, ...]) -> None:
        super().__init__(simple_logger)

        self._futures = WeakSet()
        self._events = WeakSet()
        self._user_connections = {}
        self._exc_handlers = exc_handlers

    async def connect(self, websocket: WebSocket, auth_service: AuthService) -> WebSocketContainer:
        accept_future = asyncio.gather(websocket.accept())
        await asyncio.sleep(0)

        container = WebSocketContainer(auth_service, websocket)

        await accept_future
        return container

    async def keep(self, container: WebSocketContainer) -> None:
        self._events.add(container.event)

        message_handler = self.wait_messages
        for exc_handler in self._exc_handlers[::-1]:
            message_handler = partial(exc_handler.message_handle, self, message_handler)

        while not container.event.is_set():
            try:
                await message_handler(container)

            except WebSocketDisconnect:
                container.event.set()
                if container.user_id is not None:
                    self._user_connections.pop(container.user_id, None)

        if container.websocket.client_state != WebSocketState.DISCONNECTED:
            await container.websocket.close()  # TODO add code and reason

    async def shutdown(self) -> None:
        for event in self._events:
            event.set()

        for future in self._futures:
            future.cancel()

        await asyncio.sleep(0)

    async def wait_messages(self, container: WebSocketContainer) -> None:
        future_message = asyncio.gather(container.websocket.receive_json())
        self._futures.add(future_message)
        await asyncio.sleep(0)
        self.logger.debug("resume processing")

        message = (await future_message)[0]
        self.logger.debug("future message collecting")

        protocol_container = MessageProtocolContainer(message=message)
        await self.process_message(protocol_container, container)

    async def message(self, event: asyncio.Event, container: WebSocketContainer) -> Any:
        self.logger.debug("start message waiting")
        message = await container.websocket.receive_json()
        event.set()
        self.logger.debug("got message")
        return message

    async def wait_future(self, future: asyncio.Future) -> None:
        await future

    async def process_message(
        self, protocol_container: MessageProtocolContainer, container: WebSocketContainer
    ) -> None:
        message = protocol_container.message

        match message:
            case AuthMessage():
                await self.process_auth(message, container)

            case _:
                raise NotImplementedError

    async def process_auth(self, message: AuthMessage, container: WebSocketContainer) -> None:
        user_data = await container.auth_service.auth_user(message)
        container.user_id = user_data.id
        self._user_connections[user_data.id] = container
        await self.send_message(Notification(type="auth_success"), container)

    async def send_message(self, message: BaseModel, container: WebSocketContainer) -> None:
        await container.websocket.send_json(message.model_dump_json())
        self.logger.debug(str(message))
