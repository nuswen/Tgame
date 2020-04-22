from app import db
from app import models
from app import bot
import requests
import json
import csv
from os import environ
from io import StringIO
from datetime import datetime
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
        user.lastMsgId = post.message_id
        db.session.commit()


def start(userId):
    '''
    Пытается добавить нового юзера в базу - возвращает start если вышло, если юзверь 
    уже есть - continue
    '''
    exUser = models.telegram_users.query.filter_by(userId = userId).first()
    if not exUser:
        ts = int(datetime.timestamp(datetime.utcnow()))
        newUser = models.telegram_users(userId = userId, 
                                        point = environ['start_point'],
                                        lastTime = ts,
                                        refCount = 0,
                                        patron = False,
                                        molestTimes = 0,
                                        archive = False)
        db.session.add(newUser)
        db.session.commit()
    commands = {'messages':environ['start_tag']}
    show(userId,commands)

def message(userId,data):
    user = models.teleusers.query.filter_by(Id = userId).first()
    message = data['data']['stitches'][user.Point]['content'][0]
    keys=[]
    img = None
    for i in data['data']['stitches'][user.Point]['content'][1:]:
        if 'image' in i:
            img = i['image']
        if 'option' in i:
            keys.append(i['option'])
    if keys == []:
        keys = None
    return message,keys,img

def _tryInt(string):
    try:
        num = int(string)
    except:
        num = None
    return num

def storyUp(idFileStory):
    '''
    Получает fileId загруженного файла, скачивает его, пытается разобрать его как CSV и добавляет к истории
    '''
    telePath = requests.get('https://api.telegram.org/bot'+environ['token']+'/getFile?file_id='+idFileStory)
    jTelePath = json.loads(telePath.text)
    pathFile = jTelePath['result']['file_path']
    print (pathFile)
    if pathFile[-4:] == '.csv':
        path = 'https://api.telegram.org/file/bot'+environ['token']+'/'
        csvStream = requests.get(path+pathFile,stream = True)
        vFile = StringIO(csvStream.text)
        csvFile = list(csv.reader(vFile))
        vFile.close()
        models.story.query.delete()

        for row in csvFile:

            ident,message,answers,link,timeout,branch,photo,audio,speclink,doc = row

            ident = _tryInt(ident)
            print(ident)

            if answers and not answers.isspace():
                answers = json.loads(answers)

            link = _tryInt(link)
            timeout = _tryInt(timeout)

            if speclink and not speclink.isspace():
                speclink = json.loads(speclink)
            
            newRow = models.story( 
                                    ident = ident,
                                    message = message,
                                    answers = answers,
                                    link = link,
                                    timeout = timeout,
                                    branch = branch,
                                    photo = photo,
                                    audio = audio,
                                    speclink = speclink,
                                    doc = doc)
            db.session.add(newRow)
        
        db.session.commit()

def specPost(userId,tag):
    specMessages = models.spec_answ.query.filter_by(tag = tag).all()
    specMessage = random.choice(specMessages)
    bot.send_chat_action(userId,"typing")
    time.sleep(1)
    poster(bot,userId,text=specMessage.message)

def storyGo(userId,answer = None, link=None):
    user = models.telegram_users.query.filter_by(userId = userId).first()
    storyRow = models.story.query.filter_by(ident = user.point).first()
    waiting = models.waiting.query.filter_by(userId = userId).first()
    if waiting:
        ts = int(datetime.timestamp(datetime.utcnow()))
        if (waiting.time-ts) <= 20:
            return
        if waiting.affront:
            specPost(userId,"affront")
        elif waiting.betweenBranch:
            specPost(userId,"betweenBranch")
    try:
        if answer:
            newStoryRow = models.story.query.filter_by(ident = storyRow.answers[answer]).first()
        elif link:
            newStoryRow = models.story.query.filter_by(ident = link).first()
        else:
            newStoryRow = storyRow
        
        #TODO ловить ответы не по сценарию и отправлять ответ из списка
        if not newStoryRow:
            print('не')
            return '5'
        ts = int(datetime.timestamp(datetime.utcnow()))
        user.point = newStoryRow.ident
        user.lastTime = ts
        betweenBranch = False
        affront = False
        if user.curBranch != newStoryRow.branch:
            newBranchTime = json.loads(user.branchTime)
            newBranchTime[user.curBranch].update({'end':ts})
            newBranchTime.update({newStoryRow.branch:{"start":ts}})
            newBranchTime = json.dumps(newBranchTime)
            user.branchTime = newBranchTime
            betweenBranch = True
        if newStoryRow.speclink:
            for i in newStoryRow.speclink:
                print(i)
                if i == "tag":
                    if newStoryRow.speclink[i] == "affront":
                        affront = True
        user.curBranch = newStoryRow.branch
        if newStoryRow.timeout:
            timeout = ts+newStoryRow.timeout
        else:
            timeout = ts + int(environ['std_timeout'])
        
        newTask = models.waiting(userId = userId, 
                                message = newStoryRow.message,
                                answers = newStoryRow.answers,
                                doc = newStoryRow.doc,
                                image = newStoryRow.photo,
                                audio = newStoryRow.audio,
                                time = timeout,
                                link = newStoryRow.link,
                                betweenBranch = betweenBranch,
                                affront = affront)
        db.session.add(newTask)
        db.session.commit()   
        return newStoryRow     
    except Exception as e:
        print(e)

def checkTask():
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

def molest():
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