import logging

from colorlog import ColoredFormatter

LOG_FORMAT = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"

formatter = ColoredFormatter(LOG_FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
