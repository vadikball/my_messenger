from uuid import UUID

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped

mapped_uuid = Mapped[UUID]
mapped_str = Mapped[str]


def default_postgresql_uuid_factory() -> postgresql.UUID:
    return postgresql.UUID(as_uuid=True)
