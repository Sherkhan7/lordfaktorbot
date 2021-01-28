from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update, ReplyKeyboardRemove

from config import CHANNEL_USERNAME
from DB import *
from helpers import set_user_data, wrap_tags, check_member

from replykeyboards.replykeyboardtypes import reply_keyboard_types
from replykeyboards.replykeyboardvariables import *
from inlinekeyboards import InlineKeyboard
from inlinekeyboards.inlinekeyboardvariables import *
from globals import *


def message_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    full_text = update.message.text
    text = full_text.split(' ', 1)[-1]

    if user:

        if check_member(update.effective_user.id, context):

            # Portfolio
            if text == reply_keyboard_types[client_menu_keyboard][user[LANG]][1]:
                pass

            # Xizmatlarimiz
            elif text == reply_keyboard_types[client_menu_keyboard][user[LANG]][2]:
                text = 'Xizmatlarmiz:\n' \
                       '- SMM\n' \
                       '- Telegram Bot yaratish\n' \
                       '- WEB sayt yaratish\n' \
                       '- Mobile ilovalar yaratish\n\n' \
                       f'Kanalimiz: \U0001F449  {CHANNEL_USERNAME}'

                inline_keyboard = InlineKeyboard(services_keyboard, user[LANG]).get_keyboard()

                update.message.reply_text(text, reply_markup=inline_keyboard)

            # Biz bilan aloq
            elif text == reply_keyboard_types[client_menu_keyboard][user[LANG]][3]:
                pass

            # Biz haqimizda
            elif text == reply_keyboard_types[client_menu_keyboard][user[LANG]][2]:
                pass

            else:
                thinking_emoji = '\U0001F914'
                update.message.reply_text(thinking_emoji, quote=True)

        else:
            text = f"Botdan to'liq foydalanish uchun {CHANNEL_USERNAME} kanaliga obuna bo'ling !"
            reply_keyboard = ReplyKeyboardRemove()

            update.message.reply_text(text, quote=True, reply_markup=reply_keyboard)

    else:
        reply_text = "\U000026A0 Siz ro'yxatdan o'tmagansiz !\nBuning uchun /start ni bosing."
        # "\U000026A0 Вы не зарегистрированы !\nДля этого нажмите /start\n\n" \
        # "\U000026A0 Сиз рўйхатдан ўтмагансиз !\nБунинг учун /start ни босинг"

        update.message.reply_text(reply_text)


message_handler = MessageHandler(Filters.text & (~ Filters.command), message_handler_callback)
