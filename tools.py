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


def start(userId):
    '''
    Пытается добавить нового юзера в базу - возвращает start если вышло, если юзверь 
    уже есть - continue
    '''
    exUser = models.telegram_users.query.filter_by(userId = userId).first()
    if exUser:
        return "continue"
    
    ts = int(datetime.timestamp(datetime.utcnow()))
    branchTime = {environ['start_branch']:{"start":ts}}
    branchTime = json.dumps(branchTime)
    
    newUser = models.telegram_users(userId = userId, 
                                    curBranch = environ['start_branch'], 
                                    point = environ['start_point'],
                                    lastTime = ts,
                                    branchTime = branchTime,
                                    refCount = 0,
                                    patron = False)
    
    db.session.add(newUser)
    db.session.commit()
    return "start"

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
    if pathFile[:-4] == '.csv':
        path = 'https://api.telegram.org/file/bot'+environ['token']+'/'
        csvStream = requests.get(path+pathFile,stream = True)
        vFile = StringIO(csvStream.text)
        csvFile = list(csv.reader(vFile))
        vFile.close()
        csvFile.pop(0)

        for row in csvFile:

            ident,message,answers,link,timeout,branch,photo,audio,speclink = row

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
                                    speclink = speclink)
            db.session.add(newRow)
        
        db.session.commit()

def storyGo(userId,answer = None, link=None):
    user = models.telegram_users.query.filter_by(userId = userId).first()
    storyRow = models.story.query.filter_by(ident = user.point).first()
    #try:
    if answer:
        newStoryRow = models.story.query.filter_by(ident = storyRow.answers[answer]).first()
    elif link:
        newStoryRow = models.story.query.filter_by(ident = link).first()
    else:
        newStoryRow = storyRow
    ts = int(datetime.timestamp(datetime.utcnow()))
    user.point = newStoryRow.ident
    user.lastTime = ts
    if user.curBranch != newStoryRow.branch:
        newBranchTime = user.branchTime
        newBranchTime.update({user.curBranch:ts})
        newBranchTime = json.dumps(newBranchTime)
        user.branchTime = newBranchTime
    user.curBranch = newStoryRow.branch
    if newStoryRow.timeout:
        timeout = ts+newStoryRow.timeout*1000
    else:
        timeout = None
    newTask = models.waiting(userId = userId, 
                            message = newStoryRow.message,
                            answers = newStoryRow.answers,
                            doc = newStoryRow.doc,
                            image = newStoryRow.photo,
                            audio = newStoryRow.audio,
                            time = timeout,
                            link = newStoryRow.link)
    db.session.add(user)
    db.session.add(newTask)
    db.session.commit()   
    return newStoryRow     
    #except Exception as e:
    #    return e

def checkTask():
    tasks = models.waiting.query.all()
    for task in tasks:
        ts = int(datetime.timestamp(datetime.utcnow()))
        if task.time>=ts:
            if task.link:
                poster(bot,task.userId,text=task.message,buttons=task.answers,doc=task.doc,img=task.image)
                db.session.delete(task)
                db.session.commit() 
                storyGo(task.userId,link=task.link)
            else:
                poster(bot,task.userId,text=task.message,doc=task.doc,img=task.image)
                db.session.delete(task)
                db.session.commit() 

