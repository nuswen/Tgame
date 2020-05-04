from telebot import types
from app import models
from app import db
import json


def poster(bot, chatId, text=None, buttons=None, lenRow=None, ed=False, message_id=None, doc=None, img=None):
    if buttons:
        if ed and not img and not doc:
            post = bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, parse_mode="HTML", reply_markup=inlineKeyboarder(buttons,lenRow=lenRow))
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img, parse_mode="HTML", reply_markup=inlineKeyboarder(buttons,lenRow=lenRow))
            if doc:
                bot.send_document(chat_id=chatId, data=doc, parse_mode="HTML", reply_markup=inlineKeyboarder(buttons,lenRow=lenRow))
            if text:
                post = bot.send_message(chatId, text, parse_mode="HTML", reply_markup=inlineKeyboarder(buttons,lenRow=lenRow))
    else:
        if ed and not img and not doc:
            post = bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, parse_mode="HTML")
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img)
            if doc:
                bot.send_document(chat_id=chatId, data=doc)
            if text:
                post = bot.send_message(chatId, text)
    return post

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
            keysRows[rowCount].append(types.InlineKeyboardButton(text=key, callback_data=json.dumps(row[key])))
    
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

def keyboarder(keys):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    temp = []
    for i in keys:
        temp.append(i)
    temp.reverse()
    for i in temp:
        keyboard.add(i)
    return keyboard