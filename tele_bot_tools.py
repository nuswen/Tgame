from telebot import types
from app import models
from app import db


def poster(bot, chatId, text=None, addTag=None, remTag=None, buttons=None, 
ed=False, message_id=None, doc=None, img=None):
    if addTag or remTag:
        usr = models.teleusers.query.filter_by(Id = chatId).first()
        if not usr.Tags:
            tags = []
        else:
            tags = usr.Tags

        if not addTag:
            addTag = []

        if not remTag:
            remTag = []
        
        if addTag:
            for i in addTag:
                if i not in tags:
                    tags.append(i)
        elif remTag:
            for i in tags:
                if i in remTag:
                    tags.remove(i)
        usr.Tags = tags
        db.session.add(usr)
        db.session.commit()
    
    if buttons:
        if ed and not img and not doc:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, reply_markup=keyboarder(buttons))
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img)
            if text:
                bot.send_message(chatId, text, reply_markup=keyboarder(buttons))
            if doc:
                bot.send_document(chat_id=chatId, data=doc)
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


""" def keyboarder(keys):
    keyboard = types.InlineKeyboardMarkup()
    for key in keys:
        keyboard.add(types.InlineKeyboardButton(text=key[0], callback_data=key[1]))
    return keyboard """

def keyboarder(keys):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i in keys:
        keyboard.add(i)
    return keyboard