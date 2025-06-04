import logging


def init_logger():
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():  # avoid duplicate handlers on reload
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
