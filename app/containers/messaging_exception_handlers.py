from pydantic import ValidationError

from app.exc.base import UserNotAuthenticatedException, UserNotFoundException
from app.services.messaging_exception_handlers.base import MessagingExceptionHandler

exc_handlers = (
    MessagingExceptionHandler(ValidationError),
    MessagingExceptionHandler(UserNotFoundException),
    MessagingExceptionHandler(UserNotAuthenticatedException),
)
