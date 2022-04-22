import logging

from models.user import get_user_level
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, ConversationHandler, Filters,
                          MessageHandler)
from utils.keyboard import ABORT, CONFIRM, SEND_REPORT, main_keyboard

logger = logging.getLogger(__name__)


def report_conversation_start(update: Update, context: CallbackContext):
    user_id = update.to_dict()['message']['from']['id']
    from run_bot import get_config
    try:
        TARGET_CHANNEL_ID = get_config()['telegram']['TARGET_CHANNEL_ID']
        context.user_data['TARGET_CHANNEL_ID'] = TARGET_CHANNEL_ID
    except KeyError:
        _message = 'Target channel ID has not been set in config file'
        logger.error(_message)
        update.message.reply_text(
            _message,
            reply_markup=main_keyboard(get_user_level(user_id))
        )
        return ConversationHandler.END
    update.message.reply_text(
        'Please write a message to send to the channel:',
        reply_markup=ReplyKeyboardMarkup(
            [[ABORT]],
            resize_keyboard=True
        )
    )
    return 'report_conversation_recording'


def report_conversation_recording(update: Update, context: CallbackContext):
    target_channel_id = context.user_data['TARGET_CHANNEL_ID']
    context.user_data['report'] = {'to_chat_id': target_channel_id,
                                   'from_chat_id': update.message.chat.id,
                                   'message_id': update.message.message_id}
    update.message.reply_text(
        'Confirm message sending',
        reply_markup=ReplyKeyboardMarkup(
            [[CONFIRM, ABORT]],
            resize_keyboard=True
        )
    )
    return 'report_conversation_send'


def report_conversation_send(update: Update, context: CallbackContext):
    to_chat_id = context.user_data['report'].get('to_chat_id')
    from_chat_id = context.user_data['report'].get('from_chat_id')
    message_id = context.user_data['report'].get('message_id')
    context.bot.forward_message(
        chat_id=to_chat_id,
        from_chat_id=from_chat_id,
        message_id=message_id
    )
    user_id = update.to_dict()['message']['from']['id']
    update.message.reply_text(
        'Message has been sent to channel',
        reply_markup=main_keyboard(get_user_level(user_id))
    )
    return ConversationHandler.END


def report_conversation_abort(update: Update, context: CallbackContext):
    user_id = update.to_dict()['message']['from']['id']
    update.message.reply_text(
        'Message sending canceled',
        reply_markup=main_keyboard(get_user_level(user_id))
    )
    return ConversationHandler.END


def report_conversation_fallback(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Please select one of provided options'
    )


report_conversation = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex(f'^({SEND_REPORT})$'),
                       report_conversation_start)
    ],
    states={
        'report_conversation_recording': [
            MessageHandler(Filters.regex(f'^({ABORT})$'),
                           report_conversation_abort),
            MessageHandler(
                Filters.text | Filters.photo | Filters.document,
                report_conversation_recording
            )
        ],
        'report_conversation_send': [
            MessageHandler(Filters.regex(f'^({ABORT})$'),
                           report_conversation_abort),
            MessageHandler(Filters.regex(f'^({CONFIRM})$'),
                           report_conversation_send)
        ]
    },
    fallbacks=[
        MessageHandler(
            Filters.text | Filters.photo | Filters.document,
            report_conversation_fallback
        )
    ]
)
