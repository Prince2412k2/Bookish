import logging
import sys


def configure_logger(log_level=logging.DEBUG, log_file="app.log"):
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(log_level)

    # Formatter for logs
    formatter = logging.Formatter(
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Avoid adding handlers multiple times (when using reload in FastAPI dev mode)
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
