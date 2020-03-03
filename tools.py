from app import db
from app import models

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
