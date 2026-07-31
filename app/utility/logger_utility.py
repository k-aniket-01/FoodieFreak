import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    handlers=[RichHandler()])

logger = logging.getLogger(__name__)
