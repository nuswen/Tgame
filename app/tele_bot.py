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


@bot.message_handler(commands=['ref'])
def refmsg(msg):
    ref(msg.chat.id)

@bot.message_handler(commands=['start'])
def hi_msg(msg):
    start(msg.chat.id)
    storyGo(msg.chat.id)



@bot.message_handler(content_types=['text'])
def text(msg):
    storyGo(msg.chat.id,answer=msg.text)

  
@bot.message_handler(content_types=['photo'])
def img(msg):
    if str(msg.json['chat']['id']) == environ['masterUser']:
        poster(bot,msg.chat.id,text=msg)


@bot.message_handler(content_types=['document'])
def CommandCsv(msg):
    if str(msg.json['chat']['id']) == environ['masterUser']:
        fileId = msg.json['document']['file_id']
        storyUp(fileId)
        poster(bot, msg.chat.id, text='Обновили историю')
    else:
        poster(bot, msg.chat.id, text='Ой, а что это? Давайте не будем?')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    #NewTest
    pass