from typing import Awaitable, Callable
from uuid import UUID

from app.db.models.groups import GroupsModel
from app.db.models.messages import MessagesModel

MessageLoaderType = Callable[[UUID], Awaitable[MessagesModel | None]]
GroupLoaderType = Callable[[UUID], Awaitable[GroupsModel | None]]
