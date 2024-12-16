import logging
from config import Settings
from logtail import LogtailHandler

DEFAULT_MESSAGE = "Internal Server Error"


settings = Settings()


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        logtail_handler = LogtailHandler(source_token=settings.LOG_TOKEN)
        logtail_formatter = logging.Formatter(fmt="%(message)s", datefmt="%H:%M:%S")
        logtail_handler.setFormatter(logtail_formatter)
        logtail_handler.setLevel(logging.ERROR)
        logger.addHandler(logtail_handler)

    return logger
