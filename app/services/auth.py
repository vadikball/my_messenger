from app.db.repositories.users import UsersRepo
from app.exc.base import UserNotAuthenticatedException
from app.schema.messaging import AuthMessage
from app.schema.user import UserSchema
from app.services.password_hashing import PasswordHashingService


class AuthService:
    def __init__(self, password_hashing_service: PasswordHashingService, users_repo: UsersRepo):
        self._users_repo = users_repo
        self._password_hashing_service = password_hashing_service

    async def auth_user(self, user_auth_data: AuthMessage) -> UserSchema:
        user_data = await self._users_repo.get_user_by_email(user_auth_data.email)

        if user_data.password != self._password_hashing_service.hash_password(user_auth_data.password):
            raise UserNotAuthenticatedException

        return user_data
