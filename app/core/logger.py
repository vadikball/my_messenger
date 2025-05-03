import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger


class LoggerBase:
    def __init__(self, simple_logger: "Logger"):
        self.logger = simple_logger


def get_default_logger() -> "Logger":
    default_logger = logger
    default_logger.remove()
    default_logger.add(sys.stderr, level="INFO")
    return default_logger
