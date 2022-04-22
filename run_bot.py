import logging
import traceback
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from app_logger import init_logger
from bot_command.admin import display_pending_users, make_reporter
from bot_command.reporter import report_conversation
from bot_command.user import display_help, greet_user, sing_in
from utils.keyboard import (DISPLAY_AUTH_REQUESTS, HELP, MAKE_REPORTER,
                            REQUEST_AUTH, START)

logger = logging.getLogger(__name__)


def get_config(config_path: Optional[Path] = 'settings.ini') -> ConfigParser:
    if not isinstance(config_path, Path):
        config_path = Path(config_path)
    if not config_path.exists():
        raise FileExistsError(f'File {config_path} does not exist')
    logger.warning(f'type config_path: {type(config_path)}')
    logger.warning(f'config path exist: {config_path.exists()}')
    config = ConfigParser()
    config.read(config_path)
    logger.warning(config.sections())
    return config


def main():
    logger.info('Запуск бота')
    config = get_config()
    telegram_bot = Updater(config['telegram'].get('BOT_API_KEY'))

    bot_dispatcher = telegram_bot.dispatcher

    bot_dispatcher.add_handler(report_conversation)
    bot_dispatcher.add_handler( (START,
                                              greet_user))
    bot_dispatcher.add_handler(CommandHandler(DISPLAY_AUTH_REQUESTS,
                                              display_pending_users))
    bot_dispatcher.add_handler(CommandHandler(MAKE_REPORTER, make_reporter))
    bot_dispatcher.add_handler(MessageHandler(Filters.regex(f'^({HELP})$'),
                                              display_help))
    bot_dispatcher.add_handler(MessageHandler(
        Filters.regex(f'^({REQUEST_AUTH})$'),
        sing_in
    ))

    telegram_bot.start_polling()
    telegram_bot.idle()


if __name__ == '__main__':
    init_logger()
    try:
        main()
    except Exception:
        logger.error(f'uncaught exception:\n{traceback.format_exc()}')
