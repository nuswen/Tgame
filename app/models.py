from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    answers = db.Column(db.Jsonb)
    link = db.Column(db.Integer)
    timeout = db.Column(db.Integer)
    branch = db.Column(db.Text)
    photo = db.Column(db.Text)
    audio = db.Column(db.Text)
    speclink = db.Column(db.Jsonb)
