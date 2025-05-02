from abc import abstractmethod

from pydantic import BaseModel

from app.db.declarative_base import Base


class RepoABC[ListParams: BaseModel, Domain: BaseModel, Model: Base]:
    @abstractmethod
    async def list(self, list_params: ListParams) -> list[Domain]: ...

    @abstractmethod
    def to_domain(self, row: Model) -> Domain:  # TODO change Any to sqlalchemy specific type
        ...
