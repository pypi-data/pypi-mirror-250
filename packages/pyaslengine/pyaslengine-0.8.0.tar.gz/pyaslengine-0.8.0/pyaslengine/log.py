"""pyaslengine.log"""

import logging


def get_logger(name, propagate=True):
    logger = logging.getLogger(name)
    logger.propagate = propagate
    return logger


def set_logging_level(level):
    logging.getLogger("pyaslengine").setLevel(level)
