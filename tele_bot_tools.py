from telebot import types
from app import models
from app import db
import json


def poster(bot, chatId, text=None, buttons=None, ed=False, message_id=None, doc=None, img=None):
    if buttons:
        if ed and not img and not doc:
            print(chatId)
            print(message_id)
            print(text)
            print(buttons)

            post = bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, reply_markup=inlineKeyboarder(buttons))
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img, reply_markup=inlineKeyboarder(buttons))
            if doc:
                bot.send_document(chat_id=chatId, data=doc, reply_markup=inlineKeyboarder(buttons))
            if text:
                post = bot.send_message(chatId, text, reply_markup=inlineKeyboarder(buttons))
    else:
        if ed and not img and not doc:
            post = bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text)
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img)
            if doc:
                bot.send_document(chat_id=chatId, data=doc)
            if text:
                post = bot.send_message(chatId, text)
    return post

def inlineKeyboarder(rows):
    rows = [{'hi':{'show':'ttt'},'buy':{'show':'ttt'},'lo':{'show':'ttt'}},{'hi':{'show':'ttt'},'buy':{'show':'ttt'},'lo':{'show':'ttt'}}]
    keysRows = []
    rowCount = 0

    """for row in rows:
        keysRows.append([])
        rowCount = len(keysRows)-1
        for key in row:
            keysRows[rowCount].append(types.InlineKeyboardButton(text=key, callback_data=json.dumps(keys[key])))
        print (keysRows)
    """
    a = types.InlineKeyboardButton(text='key0', callback_data='0')
    b = types.InlineKeyboardButton(text='key1', callback_data='1')
    c = types.InlineKeyboardButton(text='key2', callback_data='2')
    r = [[a,b],[c]]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(a)
    keyboard.add(b)
    keyboard.add(c)
    print (keyboard)
    return keyboard

def keyboarder(keys):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    temp = []
    for i in keys:
        temp.append(i)
    temp.reverse()
    for i in temp:
        keyboard.add(i)
    return keyboard