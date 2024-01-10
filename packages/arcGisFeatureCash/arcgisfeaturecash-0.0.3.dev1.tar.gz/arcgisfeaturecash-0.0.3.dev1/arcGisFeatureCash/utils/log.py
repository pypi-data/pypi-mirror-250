import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD at HH:mm:s}</green> | {level} | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> <level> {message}</level>",
)

if __name__ == "__main__":
    pass
