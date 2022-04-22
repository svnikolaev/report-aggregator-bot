import logging

from telegram import Update
from telegram.ext import CallbackContext
from models.user import get_users, add_user, get_user_level

from utils.keyboard import main_keyboard

logger = logging.getLogger(__name__)


def display_help(update: Update, context: CallbackContext):
    user_id = update.to_dict()['message']['from']['id']
    level = get_user_level(user_id) or 'unknown user'
    update.message.reply_text(
        f'Your system level: {level}\nUser ID: {user_id}',
        reply_markup=main_keyboard(get_user_level(user_id))
    )


def sing_in(update: Update, context: CallbackContext):
    user_id = update.to_dict()['message']['from']['id']
    users = get_users()
    if user_id not in users.keys():
        user = update.to_dict()['message'].get('from')
        add_user(user)
        update.message.reply_text(
            f'Authorization request has been sent: ID {user_id}',
            reply_markup=main_keyboard(get_user_level(user_id))
        )


def greet_user(update: Update, context: CallbackContext):
    user_id = update.to_dict()['message']['from']['id']
    logger.info('Called /start')
    update.message.reply_text(
        'Welcome',
        reply_markup=main_keyboard(get_user_level(user_id))
    )
