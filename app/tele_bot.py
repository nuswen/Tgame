from tele_bot_tools import *
from tools import *
from app import models
from app import bot
from app import db
import json
import re
import requests
from time import sleep


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    text = models.story.query().order_by(models.story.ident)[-1:]
    poster(bot, msg.chat.id, text=text)

@bot.message_handler(content_types=['text'])
def text(msg):
    pass
  
@bot.message_handler(content_types=['document'])
def CommandCsv(msg):
    fileId = msg.json['document']['file_id']
    storyAdd(fileId)
    poster(bot, msg.chat.id, text=fileId)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass