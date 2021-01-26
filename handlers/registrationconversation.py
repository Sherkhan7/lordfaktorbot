from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters

# from config import ACTIVE_ADMINS
from DB import insert_data

from filters import *
from helpers import set_user_data, wrap_tags
from languages import LANGS
from globals import *
from layouts import get_phone_number_layout
from replykeyboards import ReplyKeyboard
from replykeyboards.replykeyboardvariables import *

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def do_command(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    command = update.message.text

    if user:

        if user[LANG] == LANGS[0]:
            text = "Siz ro'yxatdan o'tgansiz"

        # if user[LANG] == LANGS[1]:
        #     text = "Вы зарегистрированы"
        #
        # if user[LANG] == LANGS[2]:
        #     text = "Сиз рўйхатдан ўтгансиз"

        text = f'\U000026A0 {text} !'

        if command == '/menu':

            if user[LANG] == LANGS[0]:
                reply_text = "Menyu"

            # if user[LANG] == LANGS[1]:
            #     reply_text = "Меню"
            #
            # if user[LANG] == LANGS[2]:
            #     reply_text = "Меню"

            text = f'\U0001F4D6 {reply_text}'

        # menu_keyboard = admin_menu_keyboard if user_data['user_data'][IS_ADMIN] else client_menu_keyboard
        menu_keyboard = client_menu_keyboard

        reply_keyboard = ReplyKeyboard(menu_keyboard, user[LANG]).get_keyboard()
        update.message.reply_text(text, reply_markup=reply_keyboard)

        state = ConversationHandler.END

    else:
        user_data[USER_INPUT_DATA] = dict()
        user_data[USER_INPUT_DATA][TG_ID] = update.effective_user.id
        user_data[USER_INPUT_DATA][USERNAME] = update.effective_user.username
        user_data[USER_INPUT_DATA][LANG] = 'uz'

        text = 'Ism va familyangizni yuboring:'
        update.message.reply_text(text)

        state = FULLNAME
        user_data[USER_INPUT_DATA][STATE] = state

        logger.info('user_data: %s', user_data)

    return state


def fullname_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data

    fullname = fullname_filter(update.message.text)

    if fullname:

        user_data[USER_INPUT_DATA][FULLNAME] = fullname

        text = "Siz bilan bog'lanishimiz uchun telefon raqamingizni yuboring\n"
        layout = get_phone_number_layout(user_data[USER_INPUT_DATA][LANG])
        reply_keyboard = ReplyKeyboard(phone_number_keyboard, user_data[USER_INPUT_DATA][LANG]).get_keyboard()
        text += layout

        # insert_data(user_data[USER_INPUT_DATA], 'users')
        # set_user_data(update.effective_user.id, user_data)

        # if user_data[USER_INPUT_DATA][LANG] == LANGS[0]:
        #     text = "Tabriklaymiz !\n" \
        #            "Siz ro'yxatdan muvofaqqiyatli o'tdingiz\n\n"

        # if user_data[USER_INPUT_DATA][LANG] == LANGS[1]:
        #     text = "Поздравляем !\n" \
        #            "Вы успешно зарегистрировались\n\n"
        #
        # if user_data[USER_INPUT_DATA][LANG] == LANGS[2]:
        #     text = "Табриклаймиз !\n" \
        #            "Сиз рўйхатдан мувофаққиятли ўтдингиз\n\n"

        # if user_data[USER_INPUT_DATA][IS_ADMIN]:
        #     text += "Buyurtmalarni qabul qilishingiz mumkin"
        #     menu_keyboard = admin_menu_keyboard
        #
        # else:
        #     text += "Kitob buyurtma qilishingiz mumkin"
        #     menu_keyboard = client_menu_keyboard

        update.message.reply_html(text, reply_markup=reply_keyboard)

        state = PHONE_NUMBER

    else:

        if user_data[USER_INPUT_DATA][LANG] == LANGS[0]:
            text = "Ism va familya xato yuborildi !\n" \
                   "Qaytadan quyidagi formatda yuboring"
            example = "Misol: Sherzodbek Esanov yoki Sherzodbek"

        # if user_data[USER_INPUT_DATA][LANG] == LANGS[1]:
        #     text = 'Имя и фамилия введено неверное !\n' \
        #            'Отправьте еще раз в следующем формате'
        #     example = 'Пример: Шерзод Эсанов'
        #
        # if user_data[USER_INPUT_DATA][LANG] == LANGS[2]:
        #     text = "Исм ва фамиля хато юборилди !\n" \
        #            "Қайтадан қуйидаги форматда юборинг"
        #     example = "Мисол: Шерзод Эсанов"

        text = f'\U000026A0 {text}:\n\n {wrap_tags(example)}'

        update.message.reply_html(text, quote=True)

        state = user_data[USER_INPUT_DATA][STATE]

    logger.info('user_data: %s', user_data)
    return state


def phone_callback(update: Update, context: CallbackContext):
    # with open('jsons/callback_query.json', 'w') as update_file:
    #     update_file.write(update.callback_query.to_json())
    user_data = context.user_data

    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    phone_number = phone_number_filter(phone_number)

    if not phone_number:

        error_text = "Telefon raqami xato formatda yuborildi\n"
        layout = get_phone_number_layout(user_data[USER_INPUT_DATA][LANG])
        error_text += layout

        update.message.reply_html(error_text, quote=True)

        state = user_data[USER_INPUT_DATA][STATE]

    else:

        user_data[USER_INPUT_DATA][PHONE_NUMBER] = phone_number

        text = "To'liq manzilingizni yuboring:\n"
        example = wrap_tags('Masalan: Toshkent shahri, Chilonzor tumani, XX-uy, XX-xonadon')
        text += example
        update.message.reply_html(text, reply_markup=ReplyKeyboardRemove())

        # layout = get_basket_layout(user_data[USER_INPUT_DATA][BASKET], user[LANG])
        # layout += f'Mijoz: {wrap_tags(user[FULLNAME])}\n' \
        #           f'Tel: {wrap_tags(user_data[USER_INPUT_DATA][PHONE_NUMBER])}\n'
        # layout += f'Telegram: {wrap_tags("@" + user[USERNAME])}' if user[USERNAME] else ''
        #
        # inline_keyboard = InlineKeyboard(confirm_keyboard, user[LANG], data=geo).get_keyboard()
        #
        # message = update.message.reply_html(layout, reply_markup=inline_keyboard)
        # user_data[USER_INPUT_DATA][MESSAGE_ID] = message.message_id

        state = ADDRESS
        user_data[USER_INPUT_DATA][STATE] = state

    logger.info('user_data: %s', user_data)
    return state


def address_callback(update: Update, context: CallbackContext):
    # with open('jsons/callback_query.json', 'w') as update_file:
    #     update_file.write(update.callback_query.to_json())
    user_data = context.user_data

    user_data[USER_INPUT_DATA][ADDRESS] = update.message.text
    # text = "Geolokatsiyangizni yuboring.\n" \
    #        f"Yoki bu bosqichni o'tkazib yuborinsh uchun {wrap_tags('keyingisi')} tugmasini bosing"

    # reply_keyboard = ReplyKeyboard(location_keyboard, user_data[USER_INPUT_DATA][LANG]).get_keyboard()
    # update.message.reply_text(context.bot.export_chat_invite_link('@mychannel_98'))
    text = f"Botdan to'liq foydalanish uchun {wrap_tags('@mychannel_98')} kanaliga obuna bo'ling\n" \
           f"Kanalga obuna bo'lganingizdan so'ng {wrap_tags('Tasdiqlash')} ni bosing"
    reply_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton('Tasdiqlash')]
    ], resize_keyboard=True)

    update.message.reply_html(text, reply_markup=reply_keyboard)

    state = CONFIRMATION

    user_data[USER_INPUT_DATA][STATE] = state

    logger.info('user_data: %s', user_data)
    return state


def confirmation_callback(update: Update, context: CallbackContext):
    # with open('jsons/callback_query.json', 'w') as update_file:
    #     update_file.write(update.callback_query.to_json())
    user_data = context.user_data

    chat_member = context.bot.get_chat_member('@mychannel_98', update.effective_user.id)
    status = chat_member.status

    if status == 'member' or status == 'creator' or status == 'administrator':

        user_data[USER_INPUT_DATA].pop(STATE)
        user_data[USER_INPUT_DATA]['is_ch_joined'] = True
        user_data[USER_INPUT_DATA][STATUS] = True

        insert_data(user_data[USER_INPUT_DATA], 'users')
        set_user_data(update.effective_user.id, user_data)
        user = user_data['user_data']

        text = f"\U0001F44F\U0001F44F\U0001F44F Tabriklaymiz siz ro'yxatdan o'tdingiz"
        menu_keyboard = client_menu_keyboard

        reply_keyboard = ReplyKeyboard(menu_keyboard, user[LANG]).get_keyboard()
        update.message.reply_text(text, reply_markup=reply_keyboard)

        state = ConversationHandler.END

        del user_data[USER_INPUT_DATA]

    else:

        update.message.reply_text("Kanalga obuna bo'ling:\n"
                                  "@mychannel_98")

        state = user_data[USER_INPUT_DATA][STATE]

    return state


registration_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['start', 'menu'], do_command, filters=~Filters.update.edited_message),
    ],
    states={

        FULLNAME: [MessageHandler(Filters.text, fullname_callback)],

        PHONE_NUMBER: [MessageHandler(Filters.contact | Filters.text & (~ Filters.command), phone_callback)],

        ADDRESS: [MessageHandler(Filters.text & (~ Filters.command), address_callback)],

        CONFIRMATION: [MessageHandler(Filters.regex('^Tasdiqlash$'), confirmation_callback)]
    },
    fallbacks=[],

    persistent=True,

    name='registration_conversation'
)
