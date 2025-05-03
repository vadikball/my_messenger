from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.declarative_base import Base
from app.schema.base import BaseFromAttrs


class RepoABC[Model: Base, Domain: BaseFromAttrs]:
    def __init__(self, async_session: AsyncSession):
        self._session = async_session

    def to_domain(self, row: Model) -> Domain:
        return self.domain.model_validate(row)

    @property
    @abstractmethod
    def domain(self) -> type[Domain]: ...
