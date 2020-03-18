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
    doc = db.Column(db.Text)


class telegram_users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    curBranch = db.Column(db.Text)
    point = db.Column(db.Integer)
    lastTime = db.Column(db.Integer)
    branchTime = db.Column(JSONB)
    refCount = db.Column(db.Integer)
    patron = db.Column(db.Boolean)
    patronId = db.Column(db.Text)

class waiting(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    answers = db.Column(JSONB)
    doc = db.Column(db.Text)
    image = db.Column(db.Text)
    audio = db.Column(db.Text)
    time = db.Column(db.Integer)
    link = db.Column(db.Integer)
    betweenBranch = db.Column(db.Boolean)