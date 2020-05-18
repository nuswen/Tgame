from os import environ
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import telebot
import threading
import time
import json

bot = telebot.TeleBot(environ['token'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)

from app import tele_bot, models

@app.before_first_request
def activate_job():
    def checkTask_worker():
        from tools import checkTask
        while True:
            checkTask()
    def molest_worker():
        from tools import molest
        while True:
            molest()

    thread = threading.Thread(target=checkTask_worker)
    thread_2 = threading.Thread(target=molest_worker)
    thread.start()
    thread_2.start()

@app.route("/"+environ['token'], methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200

@app.route("/patreon/", methods=['POST'])
def patreon():
    data= json.loads(request.stream.read().decode("utf-8"))
    print(data)
    if data['data']['type'] == 'member':
        print(data['data']['attributes']['email'])
        print(data['data']['attributes']['patron_status'])
    elif data['data']['type'] == 'pledge':
        print(data['included'][0]['attributes']['email'])
        print(data['included'][1]['amount_cents'])
    return "ok", 200

bot.remove_webhook()
bot.set_webhook(url=environ['app_url']+environ['token'])
print(environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))