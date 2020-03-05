from app import db
from sqlalchemy.dialects.postgresql import JSONB


class story(db.Model):
    ident = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    answers = db.Column(JSONB)
    link = db.Column(db.Integer)
    timeout = db.Column(db.Integer)
    branch = db.Column(db.Text)
    photo = db.Column(db.Text)
    audio = db.Column(db.Text)
    speclink = db.Column(JSONB)

class telegram_users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    curBranch = db.Column(db.Text)
    point = db.Column(db.Integer)
    lastTime = db.Column(db.TimeStamp)
    branchTime = db.Column(JSONB)
    refCount = db.Column(db.Integer)
    panron = db.Column(db.Boolean)
    patronId = db.Column(db.Text)