import logging
from typing import Optional

from telegram import ReplyKeyboardMarkup

from models.user import ADMIN, BLOCKED, PENDING, REPORTER

logger = logging.getLogger(__name__)
HELP = 'help'
REQUEST_AUTH = 'Authorization request to send reports'
ABORT = 'Abort'
CONFIRM = 'Confirm'
SEND_REPORT = 'Send message to the channel'
MAKE_REPORTER = 'make_reporter'
DISPLAY_AUTH_REQUESTS = 'display_requests'
START = 'start'


def main_keyboard(level: Optional[str] = '') -> ReplyKeyboardMarkup:
    if level == ADMIN:
        return admin_keyboard()
    elif level == REPORTER:
        return reporter_keyboard()
    elif level == PENDING:
        return pending_keyboard()
    elif level == BLOCKED:
        return blocked_keyboard()
    else:
        return default_keyboard()


def admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [f'/{DISPLAY_AUTH_REQUESTS}', f'/{MAKE_REPORTER}'],
            [SEND_REPORT],
            [HELP],
        ],
        resize_keyboard=True
    )


def reporter_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [SEND_REPORT],
            [HELP],
        ],
        resize_keyboard=True
    )


def pending_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [HELP],
        ],
        resize_keyboard=True
    )


def blocked_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [HELP],
        ],
        resize_keyboard=True
    )


def default_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [REQUEST_AUTH],
            [HELP],
        ],
        resize_keyboard=True
    )
