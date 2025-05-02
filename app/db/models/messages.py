from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.declarative_base import Base
from app.db.models.base import default_postgresql_uuid_factory, mapped_uuid
from app.db.models.chats import ChatsModel
from app.db.models.users import UsersModel


class MessagesModel(Base):
    __tablename__ = "messages"

    id: mapped_uuid = mapped_column(default_postgresql_uuid_factory(), primary_key=True, default=uuid4)
    text: Mapped[Optional[str]] = mapped_column(Text)
    sender_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(UsersModel.id, ondelete="CASCADE"), nullable=False
    )
    chat_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(ChatsModel.id, ondelete="CASCADE"), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    seen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sender: Mapped[UsersModel] = relationship(
        uselist=False,
    )
    chat: Mapped[ChatsModel] = relationship(
        uselist=False,
    )


class MessageStatusModel(Base):
    __tablename__ = "message_seen_status"

    message_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(MessagesModel.id, ondelete="CASCADE"), primary_key=True
    )
    user_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(UsersModel.id, ondelete="CASCADE"), primary_key=True
    )
