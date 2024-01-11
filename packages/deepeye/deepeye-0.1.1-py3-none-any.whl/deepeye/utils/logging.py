import os
import logging
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_folder='logs'):
    # Ensure log folder exists
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Create a logger
    logger = logging.getLogger('example_logger')
    logger.setLevel(logging.DEBUG)

    # Create a console handler with colored output
    console_handler = logging.StreamHandler()
    colored_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)

    # Create a file handler that logs messages to a file in the specified folder, rotating daily
    log_file_path = os.path.join(log_folder, 'daily_log')
    file_handler = TimedRotatingFileHandler(
        log_file_path, when="midnight", interval=1, backupCount=5)
    file_handler.suffix = "%Y-%m-%d"
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


# Setup the logger
logger = setup_logger()
