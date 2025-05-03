from asyncio import Event
from dataclasses import dataclass, field
from uuid import UUID

from fastapi import WebSocket

from app.services.auth import AuthService


@dataclass()
class WebSocketContainer:
    auth_service: AuthService

    websocket: WebSocket

    event: Event = field(default_factory=Event)
    user_id: UUID | None = None
