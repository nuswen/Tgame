from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import ARRAY


class messages(db.Model):
    tag = db.Column(db.Text, primary_key=True)
    message = db.Column(db.Text)
    buttons = db.Column(JSONB)
    edit = db.Column(db.Boolean)

class book(db.Model):
    ident = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.Text)
    firstLastWord = db.Column(JSONB)

class words(db.Model):
    ident = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Text)
    translate = db.Column(db.Text)
    sentence = db.Column(db.Integer)

class telegram_users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    point = db.Column(db.Integer)
    words = db.Column(JSONB)
    lastTime = db.Column(db.Integer)
    refCount = db.Column(db.Integer)
    patron = db.Column(db.Boolean)
    patronId = db.Column(db.Text)
    molestTimes = db.Column(db.Integer)
    archive = db.Column(db.Boolean)
    lastMsgId = db.Column(db.Integer)
    curSentence = db.Column(db.Integer)
    curStBook = db.Column(db.Integer)
    newWordsToday = db.Column(db.Integer)
    inLesson = db.Column(ARRAY(db.Text))
    molestWordDate = db.Column(db.Text)