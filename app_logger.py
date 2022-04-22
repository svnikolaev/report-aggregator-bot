import logging
import sys
from typing import Optional

LOGGING_LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO
}


def init_logger(level: Optional[str] = 'info'):
    file_handler = logging.FileHandler(filename='bot.log', encoding='utf-8')
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=LOGGING_LEVEL[level],
        format='ts=%(asctime)s level=%(levelname)s module="%(name)s:%(lineno)d" msg="%(message)s"',  # noqa E501
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=handlers
    )
