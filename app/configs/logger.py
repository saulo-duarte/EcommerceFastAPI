import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger.remove()

logger.add(
    sys.stdout,
    format="{time:ISO8601} | {level} | {message}",
    level=LOG_LEVEL,
    serialize=True,
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level=LOG_LEVEL,
    serialize=True,
    enqueue=True,
)
