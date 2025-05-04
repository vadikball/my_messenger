from abc import abstractmethod

from pydantic import JsonValue


class MessagingException(Exception):
    @abstractmethod
    def json(self) -> JsonValue: ...


class UserNotFoundException(MessagingException):
    def json(self) -> JsonValue:
        return '{"detail": "user not found"}'


class UserNotAuthenticatedException(MessagingException):
    def json(self) -> JsonValue:
        return '{"detail": "user not authenticated"}'


class AccessDeniedException(MessagingException):
    def json(self) -> JsonValue:
        return '{"detail": "access denied"}'
