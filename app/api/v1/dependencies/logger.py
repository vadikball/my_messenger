from functools import cache
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from loguru import logger

from app.core.logger import get_default_logger
from app.core.settings import settings

if TYPE_CHECKING:
    from loguru import Logger


@cache
def get_logger() -> "Logger":
    if not settings.DEBUG:
        return get_default_logger()

    return logger


LoggerDependencyType = Annotated["Logger", Depends(get_logger)]
