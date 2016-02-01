__author__ = 'justus'

from datetime import datetime


from .. import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text())

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title="", body=""):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blogpost - {}>'.format(self.title)


class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text())

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.String(100))
    image = db.Column(db.String(150))

    def __init(self, title='', body='', created_by='', image=''):
        self.title = title
        self.body = body
        self.created_by = created_by
        self.image = image

    def __repr__(self):
        return '<FAQ - {}>'.format(self.title)