from app import db
from app import models
from app import bot
import requests
import json
import csv
from conf import *
from io import StringIO
from datetime import datetime,date,timedelta
import time
from tele_bot_tools import *
import random

def show(userId,commands):
    for command in commands:
        user = models.telegram_users.query.filter_by(userId = userId).first()
        if command == 'messages':
            msg = models.messages.query.filter_by(tag = commands[command]).first() 
            if user.lastMsgId:         
                post = poster(bot,userId,msg.message,buttons=msg.buttons,ed=msg.edit, message_id=user.lastMsgId)
            else:
                post = poster(bot,userId,msg.message,buttons=msg.buttons) 
        elif command == 'nextSentence':
            user.curSentence = user.curSentence + 1
            post = sentence(user)
        elif command == 'sentence':
            post = sentence(user,ed=True, startWord=commands[command])
        elif command == 'nextWord':
            post = wordTeacher(user.userId,ed=bool(commands[command]['ed']), message_id=user.lastMsgId)
        user.lastMsgId = post.message_id
        db.session.commit()
def addWord(userId,commands,callId):
    user = models.telegram_users.query.filter_by(userId = userId).first()
    bot.answer_callback_query(callId, text=pickWordMsg)
    user.words.update({commands['word']:{'nextDate':str(date.today()),'sec':0}})
    models.telegram_users.query.filter_by(userId = userId).update({'words': user.words})
    models.telegram_users.query.filter_by(userId = userId).update({'newWordsToday': user.newWordsToday +1})
    db.session.commit()
    sentence(user,ed=True,startWord=commands['startWord'])
def sentence(user,ed=False,startWord = -1):
    book = models.book.query.filter_by(ident = user.curSentence).first()
    if startWord<0:
        startWord = book.firstLastWord['start']
    words = models.words.query.filter(models.words.ident >= startWord, 
                                        models.words.ident <= book.firstLastWord['end']).all()
    wordButtons = {}
    controlButtons = {}
    isBreak = False
    for word in words:
        if wordButtons.get(word.word):
            isBreak = True
            break
        if len(wordButtons) >= wordsAtTime:
            isBreak = True
            break
        prevLastWord = word.ident
        if str(word.ident) in user.words:
            wordButtons.update({word.translate:{'nothing':'nothing'}})
        else:
            wordButtons.update({word.word:{'addWord':{'word':word.ident,'startWord':startWord}}})
    controlButtons.update({'>>':{'show':{'nextSentence':0}}})
    if startWord != book.firstLastWord['start']:
        controlButtons.update({'<':{'show':{'sentence':startWord-wordsAtTime}}})
    if isBreak:
        controlButtons.update({'>':{'show':{'sentence':prevLastWord+1}}})
    buttons = [wordButtons,controlButtons]
    if ed:
        post = poster(bot,user.userId,book.sentence,buttons=buttons,ed=ed,message_id=user.lastMsgId,lenRow=wordsInRow)
    else:
        post = poster(bot,user.userId,book.sentence,buttons=buttons,lenRow=wordsInRow)
    return post
def start(userId):
    '''
    Пытается добавить нового юзера в базу - возвращает start если вышло, если юзверь 
    уже есть - continue
    '''
    exUser = models.telegram_users.query.filter_by(userId = userId).first()
    if not exUser:
        ts = int(datetime.timestamp(datetime.utcnow()))
        newUser = models.telegram_users(userId = userId, 
                                        point = startPoint,
                                        words = {},
                                        lastTime = ts,
                                        refCount = 0,
                                        patron = False,
                                        molestTimes = 0,
                                        archive = False,
                                        curSentence = 0,
                                        curStBook = 0,
                                        newWordsToday = 0,
                                        inLesson = [])
        db.session.add(newUser)
        db.session.commit()
    commands = {'messages':startTag}
    show(userId,commands)
def wordTeacher(userId,ed=False,message_id=None):
    user = models.telegram_users.query.filter_by(userId = userId).first()
    butWords ={}
    wordsNum = []
    sentenceNum = -1
    words = []
    today = str(date.today())
    for wordNum in user.words:
        word = models.words.query.filter_by(ident = int(wordNum)).first()
        if wordNum not in user.inLesson and sentenceNum == -1 and user.words[wordNum]['nextDate'] == today:
            sentenceNum = word.sentence
            wordsNum.append(int(wordNum))
            user.inLesson.append(wordNum)
            words.append(word.word)
            butWords.update({word.word:{'flashTrns':wordNum}})
            continue
        if wordNum not in user.inLesson and sentenceNum == word.sentence and user.words[wordNum]['nextDate'] == today:
            wordsNum.append(int(wordNum))
            user.inLesson.append(wordNum)
            words.append(word.word)
            butWords.update({word.word:{'flashTrns':wordNum}})
    if butWords == {}:
        post = wordEnder(userId,ed=ed,message_id=message_id)
    else:
        book = models.book.query.filter_by(ident = sentenceNum).first()
        msg = book.sentence
        for word in words:
            spltmsg = msg.split(word)
            for i in range(0,len(spltmsg)-1,2):
                msg = spltmsg[i] + '*'+word+'*'+spltmsg[i+1]

        models.telegram_users.query.filter_by(userId = userId).update({'inLesson': user.inLesson})
        db.session.commit()
        
        buttons = [butWords,{'>>':{'show':{'nextWord':{'ed':True}}}}]
        post = poster(bot,userId,msg,buttons=buttons,ed=ed,message_id=message_id) 
    return post
def flashTrns(userId,wordNum,callId):
    word = models.words.query.filter_by(ident = int(wordNum)).first()
    user = models.telegram_users.query.filter_by(userId = userId).first()
    user.words.update({wordNum:{'sec':0,'nextDate':str(date.today()+timedelta(days=1))}})
    models.telegram_users.query.filter_by(userId = userId).update({'words': user.words})
    db.session.commit()

    bot.answer_callback_query(callId, text=word.translate)

def wordEnder(userId,ed=False,message_id=None):
    user = models.telegram_users.query.filter_by(userId = userId).first()
    for wordNum in user.inLesson:
        if user.words[wordNum]['sec']<90:
            curDate = datetime.strptime(user.words[wordNum]['nextDate'],'%Y-%m-%d')
            user.words[wordNum]['sec'] = user.words[wordNum]['sec'] + 10
            if user.words[wordNum]['sec']<70:
                nextDate = curDate + timedelta(days=1)
            else:
                nextDate = curDate + timedelta(days=14)
            user.words[wordNum]['nextDate'] = str(nextDate.date)
        elif user.words[wordNum]['sec']>=90:
            user.words.pop(wordNum)
    user.inLesson = []
    db.session.commit()
    buttons = [{'Главная кнопка':{'Ничего':1}}]
    post = poster(bot,userId,textWordEnd,buttons=buttons,ed=ed,message_id=message_id) 
    return post


"""def checkTask():
    ts = int(datetime.timestamp(datetime.utcnow()))
    tasks = models.waiting.query.all()
    for task in tasks:
        if task.time<=ts:
            if task.link:
                poster(bot,task.userId,text=task.message,buttons=task.answers,doc=task.doc,img=task.image)
                db.session.delete(task)
                db.session.commit() 
                storyGo(task.userId,link=task.link)
            else:
                poster(bot,task.userId,text=task.message,buttons=task.answers,doc=task.doc,img=task.image)
                db.session.delete(task)
                db.session.commit()
                continue
        elif (task.time-ts)<15:
            if task.image:
                bot.send_chat_action(task.userId,"upload_photo")
            elif task.audio:
                bot.send_chat_action(task.userId,"record_audio")
            elif task.doc:
                bot.send_chat_action(task.userId,"upload_document")
            elif task.message:
                bot.send_chat_action(task.userId,"typing")
    time.sleep(1)
"""

"""def molest():
    ts = int(datetime.timestamp(datetime.utcnow()))
    #TODO Можно не вытаскивать архивные строячки (molestTimes>4)
    users = models.telegram_users.query.all()
    for user in users:
        if ts-user.lastTime>int(environ['first_molest']) and user.molestTimes==0:
            user.molestTimes = 1
            specPost(user.userId,'first_molest')
            storyGo(user.userId)
        elif ts-user.lastTime>int(environ['second_molest']) and user.molestTimes==1:
            user.molestTimes = 2
            specPost(user.userId,'second_molest')
            storyGo(user.userId)
        elif ts-user.lastTime>int(environ['third_molest']) and user.molestTimes==2:
            user.molestTimes = 3
            specPost(user.userId,'third_molest')
            branchTime = json.loads(user.branchTime)
            for branch in branchTime:
                if 'end' not in branchTime[branch]:
                    startBranchMsg = models.story.query.filter_by(branch = branch).order_by(models.story.ident).first()
                    user.point = startBranchMsg.ident
                    branchTime.pop(branch)
                    user.branchTime = json.dumps(branchTime)
                    break
        #Сутки спустя
        elif ts-user.lastTime>86400 and user.molestTimes==3:
            user.molestTimes = 4
        #Месяц спустя
        elif ts-user.lastTime>2592000 and user.molestTimes==4:
            new_arc = models.arc_telegram_users(userId = user.userId, 
                                                curBranch = user.curBranch, 
                                                point = user.point,
                                                lastTime = user.lastTime,
                                                branchTime = user.branchTime,
                                                refCount = user.refCount,
                                                patron = user.patron,
                                                molestTimes = user.molestTimes)
            branchTime = {environ['start_branch']:{"start":ts}}
            branchTime = json.dumps(branchTime)
            user.curBranch = environ['start_branch']
            user.point = environ['start_point']
            user.branchTime = branchTime
            user.molestTimes = 5
            db.session.add(new_arc)
            
    db.session.commit()
    time.sleep(10)
"""