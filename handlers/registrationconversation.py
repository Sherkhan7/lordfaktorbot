from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters

# from config import ACTIVE_ADMINS
# from DB import insert_data

# from filters import *
# from helpers import set_user_data, wrap_tags
# from languages import LANGS
# from globalvariables import *
# from replykeyboards import ReplyKeyboard
# from replykeyboards.replykeyboardvariables import *

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def do_command(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data
    # set_user_data(update.effective_user.id, user_data)
    # user = user_data['user_data']

    command = update.message.text

    update.message.reply_text('Salom')


registration_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['start', 'menu'], do_command, filters=~Filters.update.edited_message),
    ],
    states={

        # FULLNAME: [MessageHandler(Filters.text, fullname_callback)],
    },
    fallbacks=[],

    persistent=True,

    name='registration_conversation'
)
