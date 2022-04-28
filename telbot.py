import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

load_dotenv()
token = os.getenv('TOKEN')
updater = Updater(token)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello im Xenrix, type /help to see what i can do")

def _help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available Commands :-
    /youtube - To get the youtube URL
    /linkedin - To get the LinkedIn profile URL
    /gmail - To get gmail URL
    /geeks - To get the GeeksforGeeks URL"""
  
    )

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", _help))

updater.start_polling()