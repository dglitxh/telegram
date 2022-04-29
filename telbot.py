import json
import os
import requests
import logging
import wolframalpha
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

def compute(update: Update, context: CallbackContext, ):
    question = " ".join(context.args)
    app_id = "E8H76X-T8V8UHPUY2"
    client = wolframalpha.Client(app_id)
    try:
        req = client.query(question)
        res = next(req.results).text
        print(question, res)
        update.message.reply_text(res)
    except:
        logging.error("could not find an answer on wolfram")
        update.message.reply_text("Errm... dont know about that one buddy 😬😬")

def get_weather (update: Update, context: CommandHandler):
    loc = " ".join(context.args)
    apiKey = 'ea21c2ee64bf2fd0f38674dc16e62852'
    try:
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={apiKey}")
        data = json.loads(req.text)
        weather = {
        'weather': f"Weather:  {data['weather'][0]['main']}",
            'country': f"Country:  {data['sys']['country']}",
            'location': f"City:  {data['name']}",
            'weatherDesc': f"Desc:  {data['weather'][0]['description']}",
            'temperature': f"Temp:  {round(data['main']['temp'] - 273.15)}°С",
            'humidity': f"Humidity:  {data['main']['humidity']}%",
            'feel': f"Feels like:  {round(data['main']['feels_like'] - 273.15)}°С",
            'windSpeed': f"Wind:  {data['wind']['speed']}km/h" 
        }
        msg = f"Weather in {loc.title()}\n********************\n"
        for i in weather:
            msg += weather[i] + "\n\n"
        update.message.reply_text(msg)
    except:
        logging.error("could not find weather on open weather")
        update.message.reply_text("Errm... couldn't find weather check spelling and/or try again 😬😬")

def _help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available Commands :-
    /help - get help on how to use bot.
    /quote - get an inspirational quote.
    /compute - Ask and get answers to your math and scientific questions
    """
  
    )

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", _help))
updater.dispatcher.add_handler(CommandHandler("quote", quote))
updater.dispatcher.add_handler(CommandHandler("compute", compute))
updater.dispatcher.add_handler(CommandHandler("weather", get_weather))

updater.start_polling()

print("We are live!!")

updater.idle()