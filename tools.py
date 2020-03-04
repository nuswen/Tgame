from app import db
from app import models
import requests
import json
import csv
from os import environ
from io import StringIO


def start(userId,data):
    '''
    Пытается добавить нового юзера в базу - возвращает start если вышло, если юзверь 
    уже есть - continue
    '''
    exUser = models.teleusers.query.filter_by(Id = userId).first()
    if exUser:
        return
    playPoint = data['data']['initial']
    newUser = models.teleusers(Id = userId, Point = playPoint, Tags = [])
    db.session.add(newUser)
    db.session.commit()
    return

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

def tryInt(string):
    try:
        num = int(string)
    except:
        num = None
    return num

def storyUp(idFileStory):
    telePath = requests.get('https://api.telegram.org/bot'+environ['token']+'/getFile?file_id='+idFileStory)
    jTelePath = json.loads(telePath.text)
    pathFile = jTelePath['result']['file_path']
    path = 'https://api.telegram.org/file/bot'+environ['token']+'/'
    csvStream = requests.get(path+pathFile,stream = True)
    vFile = StringIO(csvStream.text)
    csvFile = list(csv.reader(vFile))
    vFile.close()
    csvFile.pop(0)

    for row in csvFile:

        ident,message,answers,link,timeout,branch,photo,audio,speclink = row

        ident = tryInt(ident)
        print(ident)

        if answers or answers.isspace():
            answers = json.loads(answers)

        link = tryInt(link)
        timeout = tryInt(timeout)

        if speclink or speclink.isspace():
            speclink = json.loads(speclink)

        allStary = models.query.all()
        for row in allStary:
            db.session.delete(row)
        
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