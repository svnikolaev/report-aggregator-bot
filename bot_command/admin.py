import logging

from models.user import (PENDING, REPORTER, get_user_level, get_users,
                         is_admin, set_user_level)
from telegram import Update
from telegram.ext import CallbackContext
from utils.keyboard import main_keyboard

logger = logging.getLogger(__name__)


def display_pending_users(update: Update, context: CallbackContext):
    user_id = update.to_dict()['message']['from']['id']
    if is_admin(user_id):
        pending_users = get_users(level=PENDING)
        if pending_users:
            i = 1
            message = ['Requested authorization to send reports:']
            for user in pending_users.values():
                line = f'{i}. @{user.get("username")} ID {user.get("id")}'
                name = []
                for item in [user.get("first_name"), user.get("last_name")]:
                    if item:
                        name.append(item)
                line += f' - {" ".join(name)}' if name else ''
                message.append(line+';')
                i += 1
            message = '\n'.join(message)
        else:
            message = 'No new authorization requests'
        update.message.reply_text(
            message,
            reply_markup=main_keyboard(get_user_level(user_id))
        )


def make_reporter(update: Update, context: CallbackContext):
    correctly = True
    user_id = update.to_dict()['message']['from']['id']
    if is_admin(user_id):
        try:
            promoting_user = update.message.text.split(' ')[1]
            int(promoting_user)
        except (ValueError, IndexError):
            correctly = False
            update.message.reply_text(
                'Enter the command in the format "/command user_id"',
                reply_markup=main_keyboard(get_user_level(user_id))
            )
        if correctly:
            set_user_level(promoting_user, REPORTER)
            update.message.reply_text(
                'User status changed',
                reply_markup=main_keyboard(get_user_level(user_id))
            )
