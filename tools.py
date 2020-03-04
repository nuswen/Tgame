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

def storyAdd(idFileStory):
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
        if row[2]:
            row[2] = json.loads(row[2])
        if row[8]:
            row[8] = json.loads(row[8])
        newRow = models.story( 
                                ident = int(row[0]),
                                message = row[1],
                                answers = row[2],
                                link = int(row[3]),
                                timeout = int(row[4]),
                                branch = row[5],
                                photo = row[6],
                                audio = row[7],
                                speclink = row[8])
        db.session.add(newRow)
    
    db.session.commit()
        
