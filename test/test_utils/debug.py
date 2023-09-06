# all the debug functions go here
from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="DEBUG",
    format="<yellow>[sentzi-log]</yellow> <green>[{time:DD-MMM-YYYY HH:mm:ss}]</green> <level>[{level}]</level> <level>{message}</level>",
    colorize=True
)
