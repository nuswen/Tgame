from tele_bot_tools import *
from tools import *
from app import models
from app import bot
from app import db
import json
import re
import requests
from time import sleep
from os import environ

@bot.message_handler(commands=['start'])
def hi_msg(msg):
    start(msg.chat.id)

@bot.message_handler(content_types=['text'])
def text(msg):
    pass

@bot.message_handler(content_types=['photo'])
def img(msg):
    pass

@bot.message_handler(content_types=['document'])
def CommandCsv(msg):
    pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    commands = json.loads(call.data)
    for command in commands:
        if command == 'show':
            show(call.message.chat.id,commands[command])