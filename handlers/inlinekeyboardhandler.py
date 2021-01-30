from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup

from config import CHANNEL_USERNAME
from DB import *

from helpers import wrap_tags, set_user_data, check_member
from inlinekeyboards import InlineKeyboard
from inlinekeyboards.inlinekeyboardvariables import *
from globals import *

import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def inline_keyboards_handler_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    callback_query = update.callback_query
    data = callback_query.data

    # with open('jsons/callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())

    if user and check_member(update.effective_user.id, context):

        match_obj_2 = re.search(r'[rc]_[yn]_\d+$', data)
        match_obj_3 = re.search(r'^w_\d+$', data)
        match_obj_4 = re.search(r'^h_w_\d+$', data)

    else:
        callback_query.answer(f"Siz {CHANNEL_USERNAME} kanaliga a'zo emassiz !\n\n"
                              f"Botdan to'liq foydalanish uchun {CHANNEL_USERNAME} kanaligi a'zo bo'ling !\n\n",
                              show_alert=True)

    # logger.info('user_data: %s', user_data)


inline_keyboard_handler = CallbackQueryHandler(inline_keyboards_handler_callback)
