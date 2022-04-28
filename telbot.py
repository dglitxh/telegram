import json
import os
import requests
from dotenv import load_dotenv
from setuptools import Command
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

def quote(update: Update, context: CallbackContext):
    req = requests.get("https://zenquotes.io/api/random")
    res = json.loads(req.text)[0]
    msg = f"{res['q']}\n\n    ~ {res['a']}"
    update.message.reply_text(msg)

def _help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available Commands :-
    /help - get help on how to use bot.
    /quote - get an inspirational quote.
    """
  
    )

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", _help))
updater.dispatcher.add_handler(CommandHandler("quote", quote))

updater.start_polling()
print("We are live!!")