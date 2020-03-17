from os import environ
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import telebot
import threading
import time

bot = telebot.TeleBot(environ['token'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)

from app import tele_bot, models

@app.before_first_request
def activate_job():
    def run_job():
        from tele_bot_tools import *
        while True:
            poster(bot, 2601798, text='hi')
            time.sleep(3)

    thread = threading.Thread(target=run_job)
    thread.start()

@app.route("/"+environ['token'], methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

bot.remove_webhook()
bot.set_webhook(url=environ['app_url']+environ['token'])
print(environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))