from abc import abstractmethod
from asyncio import Lock
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.db.declarative_base import Base
from app.schema.base import BaseFromAttrs


class RepoABC[Model: Base, Domain: BaseFromAttrs]:
    def __init__(self, async_session: AsyncSession, lock: Lock):
        self._session = async_session
        self._lock = lock

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSessionTransaction]:
        async with self._lock:
            async with self._session.begin_nested() as transaction:
                try:
                    yield transaction
                except Exception as exc:
                    await transaction.rollback()
                    raise exc

            await self._session.commit()

    def to_domain(self, row: Model) -> Domain:
        return self.domain.model_validate(row)

    @property
    @abstractmethod
    def domain(self) -> type[Domain]: ...
