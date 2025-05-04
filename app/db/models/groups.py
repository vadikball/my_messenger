from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.base import DEFAULT_STRING_LENGTH
from app.db.declarative_base import Base
from app.db.models.base import default_postgresql_uuid_factory, mapped_str, mapped_uuid
from app.db.models.chats import ChatsModel
from app.db.models.users import UsersModel


class UserGroupModel(Base):
    __tablename__ = "user_group"

    group_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(UsersModel.id, ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class GroupsModel(Base):
    """
    Groups Model.
    Batch size of user_group must be applied dynamically at the query level.
    """

    __tablename__ = "groups"

    id: mapped_uuid = mapped_column(default_postgresql_uuid_factory(), primary_key=True, default=uuid4)
    name: mapped_str = mapped_column(String(DEFAULT_STRING_LENGTH), nullable=False)
    creator_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(UsersModel.id, ondelete="CASCADE"), nullable=False
    )
    chat_id: mapped_uuid = mapped_column(
        default_postgresql_uuid_factory(), ForeignKey(ChatsModel.id, ondelete="CASCADE"), nullable=False
    )
    user_group: Mapped[List[UserGroupModel]] = relationship(
        cascade="all, delete-orphan",
        lazy="dynamic",
        passive_deletes=True,
        order_by=UserGroupModel.created_at,
    )
