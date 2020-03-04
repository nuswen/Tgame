from app import db
from sqlalchemy.dialects.postgresql import JSONB
import requests
import json
import csv
from os import environ
from io import StringIO
from tools import *


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