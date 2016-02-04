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


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    sizes = db.Column(db.Enum('xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl', name='select_size'))
    colors = db.Column(db.Enum('red', 'blue', 'green', 'brown', 'white', 'black', name='select_color'))
    shortdesc = db.Column(db.String(100), nullable=False)
    longdesc = db.Column(db.Text())
    thumbnail = db.Column(db.String(255))
    image = db.Column(db.String(255))
    status = db.Column(db.Enum('active', 'inactive', name='set_status'), default='inactive')
    category_id = db.Column(db.Integer())
    featured = db.Column(db.Enum('true', 'false', name='set_featured'), default='false')
    price = db.Column(db.Float(4, 2))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    viewed = db.Column(db.Integer())
    viewed_ip = db.Column(db.Integer())
    product_nr = db.Column(db.Integer())

    def __init__(self, name, shortdesc, longdesc, price):
        self.name = name
        self.shortdesc = shortdesc
        self.longdesc = longdesc
        # self.thumbnail = thumbnail
        # self.image = image
        # self.category_id = category_id
        # self.featured = featured
        self.price = price
        # self.viewed = viewed
        # self.viewed_ip = viewed_ip
        # self.product_nr = product_nr

    def __repr__(self):
        return '<Products - {}>'.format(self.name, self.shortdesc, self.longdesc, self.category_id, self.price)


class Test(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image = db.Column(db.LargeBinary)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<Test - {}>'.format(self.image)