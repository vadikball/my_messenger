from asyncio import Event
from dataclasses import dataclass, field
from uuid import UUID

from fastapi import WebSocket

from app.db.repositories.chats import ChatMembersRepo
from app.db.repositories.messages import MessagesRepo
from app.services.auth import AuthService
from app.services.group import GroupsService


@dataclass()
class WebSocketContainer:
    auth_service: AuthService
    messages_repo: MessagesRepo
    chat_members_repo: ChatMembersRepo
    groups_service: GroupsService

    websocket: WebSocket

    event: Event = field(default_factory=Event)
    user_id: UUID | None = None
