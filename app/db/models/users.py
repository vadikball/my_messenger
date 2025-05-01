from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from app.constants.base import DEFAULT_STRING_LENGTH
from app.db.declarative_base import Base
from app.db.models.base import default_postgresql_uuid_factory, mapped_str, mapped_uuid


class UsersModel(Base):
    __tablename__ = "users"

    id: mapped_uuid = mapped_column(default_postgresql_uuid_factory(), primary_key=True)
    name: mapped_str = mapped_column(String(DEFAULT_STRING_LENGTH), nullable=False)
    email: mapped_str = mapped_column(String(DEFAULT_STRING_LENGTH), nullable=False, unique=True)
    password: mapped_str = mapped_column(String(DEFAULT_STRING_LENGTH), nullable=False)
