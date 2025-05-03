from sqlalchemy import select

from app.db.models.users import UsersModel
from app.db.repositories.abc import RepoABC
from app.exc.base import UserNotFoundException
from app.schema.user import UserSchema


class UsersRepo(RepoABC):
    domain = UserSchema

    async def get_user_by_email(self, email: str) -> UserSchema:
        stmt = select(UsersModel).where(UsersModel.email == email)
        user_from_db = await self._session.scalar(stmt)

        if user_from_db is None:
            raise UserNotFoundException

        return self.to_domain(user_from_db)
