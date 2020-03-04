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
    
    def upStory(self, idFileStory):
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

            
            newRow = self( 
                                    ident = ident,
                                    message = message,
                                    answers = answers,
                                    link = link,
                                    timeout = timeout,
                                    branch = branch,
                                    photo = photo,
                                    audio = audio,
                                    speclink = speclink
            db.session.add(newRow)
        CurStory = self.query.all()
        for row in CurStory:
            db.session.delete(row)

        db.session.commit()