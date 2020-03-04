from app import db
from sqlalchemy.dialects.postgresql import JSONB


class story(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    answers = db.Column(JSONB)
    link = db.Column(db.Integer)
    timeout = db.Column(db.Integer)
    branch = db.Column(db.Text)
    photo = db.Column(db.Text)
    audio = db.Column(db.Text)
    speclink = db.Column(JSONB)
