from asyncio import Barrier, Event
from dataclasses import dataclass, field
from uuid import UUID

from fastapi import WebSocket

from app.db.repositories.chats import ChatMembersRepo
from app.db.repositories.messages import MessagesRepo
from app.services.auth import AuthService
from app.services.group import GroupsService


def new_ws_container_barrier() -> Barrier:
    return Barrier(2)


@dataclass()
class WebSocketContainer:
    auth_service: AuthService
    messages_repo: MessagesRepo
    chat_members_repo: ChatMembersRepo
    groups_service: GroupsService

    websocket: WebSocket

    event: Event = field(default_factory=Event)
    new_message_event: Event = field(default_factory=Event)
    user_id: UUID | None = None

    async def wait_barrier(self) -> None:
        await self.new_message_event.wait()
        self.new_message_event.clear()
