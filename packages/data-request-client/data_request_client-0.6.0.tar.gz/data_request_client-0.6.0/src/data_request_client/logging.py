import logging

from rich.console import Console
from rich.logging import RichHandler

logging_console = Console()


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    root_logger = logging.getLogger("data_request_client")
    root_logger.setLevel(level)
    handler = RichHandler(console=logging_console)
    root_logger.addHandler(handler)

    return root_logger
