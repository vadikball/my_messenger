from typing import Any, Callable, Coroutine

from app.containers.web_socket import WebSocketContainer

MessagingHandlerType = Callable[[WebSocketContainer], Coroutine[Any, Any, None]]
