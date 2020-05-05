from telebot import types
from app import models
from app import db
import json
import re


def poster(bot, chatId, text=None, buttons=None, ed=False, message_id=None, doc=None, img=None,inline=False,lenRow=None):
    if buttons:
        if ed and not img and not doc:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, reply_markup=keyboarder(buttons,inline,lenRow))
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img, reply_markup=keyboarder(buttons,inline,lenRow))
            if text:
                bot.send_message(chatId, text, reply_markup=keyboarder(buttons,inline,lenRow))
            if doc:
                bot.send_document(chat_id=chatId, data=doc, reply_markup=keyboarder(buttons,inline,lenRow))
    else:
        if ed and not img and not doc:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text)
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img)
            if text:
                bot.send_message(chatId, text)
            if doc:
                bot.send_document(chat_id=chatId, data=doc)

def keyboarder(keys,inline,lenRow):
    if inline: 
        return inlineKeyboarder(keys,lenRow=lenRow)
    else: 
        return clasicKeyboarder(keys)

def isUrl(text):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE)
    return re.match(regex, text) is not None

def inlineKeyboarder(rows, lenRow=None):
    if not lenRow: lenRow=10
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = lenRow
    keysRows = []
    rowCount = 0

    for row in rows:
        keysRows.append([])
        rowCount = len(keysRows)-1
        for key in row:
            keyValue = json.dumps(row[key])
            print(keyValue)
            print(isUrl(keyValue))
            if isUrl(keyValue):
                keysRows[rowCount].append(types.InlineKeyboardButton(text=key, url=keyValue))
            else:
                keysRows[rowCount].append(types.InlineKeyboardButton(text=key, callback_data=keyValue))
    
    for row in keysRows:
        if len(row) == 1:
            keyboard.add(row[0])
        elif len(row) == 2:
            keyboard.add(row[0],row[1])
        elif len(row) == 3:
            keyboard.add(row[0],row[1],row[2])
        elif len(row) == 4:
            keyboard.add(row[0],row[1],row[2],row[3])
        elif len(row) == 5:
            keyboard.add(row[0],row[1],row[2],row[3],row[4])
        elif len(row) == 6:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5])
        elif len(row) == 7:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        elif len(row) == 8:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        elif len(row) == 9:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        elif len(row) == 10:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
            
    return keyboard

def clasicKeyboarder(keys):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    temp = []
    for i in keys:
        temp.append(i)
    temp.reverse()
    for i in temp:
        keyboard.add(i)
    return keyboard