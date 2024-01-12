import logging
import os
from sys import stdout

_name_to_level = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

logger = logging.getLogger('python_sdk')
logger.propagate = False

log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
console_formatter = logging.Formatter(log_format)

console_handler = logging.StreamHandler(stream=stdout)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

log_level = _name_to_level.get(os.environ.get('log_level'), logging.WARNING)
logging.captureWarnings(True)


def get_logger(log_name, level=log_level):
    module_logger = logger.getChild(log_name)
    module_logger.setLevel(level)
    return module_logger
