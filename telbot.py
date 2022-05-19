from email import message
import json
import os
import requests
import logging
import wolframalpha
from dotenv import load_dotenv
from telegram.constants import ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    PollAnswerHandler,
    PollHandler,
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
def image (update: Update, context: CallbackContext):
    img = 'https://picsum.photos/200/300/?random'
    update.message.reply_photo(img)
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
        update.message.reply_text("Errm... dont know about that one buddy 😬😬. type /help for help")

def get_weather (update: Update, context: CommandHandler):
    loc = " ".join(context.args)
    apiKey = 'ea21c2ee64bf2fd0f38674dc16e62852'
    try:
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={apiKey}")
        data = json.loads(req.text)
        weather = {
        'weather': f"Atmosphere:  {data['weather'][0]['main']}",
            'country': f"Country:  {data['sys']['country']}",
            'location': f"City:  {data['name']}",
            'weatherDesc': f"Desc:  {data['weather'][0]['description']}",
            'temperature': f"Temp:  {round(data['main']['temp'] - 273.15)}°С",
            'humidity': f"Humidity:  {data['main']['humidity']}%",
            'feel': f"Feels like:  {round(data['main']['feels_like'] - 273.15)}°С",
            'windSpeed': f"Wind:  {data['wind']['speed']}km/h" 
        }
        msg = f"{'*'*12}\nWeather in {loc.title()}\n{'*'*12}\n"
        for i in weather:
            msg += weather[i] + "\n\n"
        update.message.reply_text(msg)
    except:
        logging.error("could not find weather on open weather")
        update.message.reply_text("Errm... couldn't find weather check spelling and/or try again 😬😬. type /help for help")

def poll(update: Update, context: CallbackContext):
    try:
        qm = [x for x in context.args if "?" in x][0]
        ind = context.args.index(qm)
        questions = [' '.join(x.split('-')) for x in context.args[ind+1:]]
        print(questions)
        message = context.bot.send_poll(
            update.effective_chat.id,
            " ".join(context.args[:ind+1]),
            questions,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        payload = {
            message.poll.id: {
                "questions": questions,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0,
            }
        }
    except:
        logging.error("/Poll: could not create poll due to errors")
        update.message.reply_text("could not create poll due to errors. type /help for help")

    context.bot_data.update(payload)

async def receive_poll_answer(update: Update, context: CallbackContext) -> None:
    """Summarize a users poll vote"""
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + " and "
        else:
            answer_string += questions[question_id]
    await context.bot.send_message(
        answered_poll["chat_id"],
        f"{update.effective_user.mention_html()} feels {answer_string}!",
        parse_mode=ParseMode.HTML,
    )
    answered_poll["answers"] += 1
    # Close poll after three participants voted
    if answered_poll["answers"] == 10:
        await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])

def _help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available Commands :-
    /help - get help on how to use bot.
    /image - get a random image
    /quote - get an inspirational quote.
    /poll <question? comma separated answers use (-) to separate multiple worded answers)>
     - create a poll(eg: who am i? a-bot, a-rabbit, man)
    /compute <question> - Ask and get answers to your math and scientific questions (eg. what is an atom, 6 + 3)
    /weather <city> - Find weather in any city (eg. /weather Accra)
    """
  
    )

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", _help))
updater.dispatcher.add_handler(CommandHandler("quote", quote))
updater.dispatcher.add_handler(CommandHandler("compute", compute))
updater.dispatcher.add_handler(CommandHandler("weather", get_weather))
updater.dispatcher.add_handler(CommandHandler("image", image))
updater.dispatcher.add_handler(CommandHandler("poll", poll))
updater.dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))

updater.start_polling()

print("We are live!!")

updater.idle()