from uuid import uuid4

from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.base import DEFAULT_STRING_LENGTH
from app.db.declarative_base import Base
from app.db.models.base import default_postgresql_uuid_factory, mapped_str, mapped_uuid
from app.db.models.users import UsersModel


class ChatsModel(Base):
    __tablename__ = "chats"

    id: mapped_uuid = mapped_column(default_postgresql_uuid_factory(), primary_key=True, default=uuid4)
    name: mapped_str = mapped_column(String(DEFAULT_STRING_LENGTH), nullable=False)
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class ChatMembersModel(Base):
    __tablename__ = "chat_members"

    chat_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(ChatsModel.id, ondelete="CASCADE"), primary_key=True
    )
    user_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(UsersModel.id, ondelete="CASCADE"), primary_key=True
    )
