from abc import abstractmethod

from pydantic import BaseModel

from app.containers.web_socket import WebSocketContainer


class MessagingServiceABC:
    @abstractmethod
    async def send_message(self, message: BaseModel, container: WebSocketContainer) -> None: ...
