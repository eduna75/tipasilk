__author__ = 'justus'

from datetime import datetime
from .. import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    image = db.Column(db.LargeBinary)

    def __init__(self, title="", body=""):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blogpost - {}>'.format(self.title)


class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    image = db.Column(db.String(150))  # Probably want to use one table to hold all images uploaded.

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
    shortdesc = db.Column(db.String(100), nullable=False)
    longdesc = db.Column(db.Text())
    status = db.Column(db.Boolean, default=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    featured = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Float)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    product_nr = db.Column(db.Text, unique=True)
    images = db.relationship('Images', backref=db.backref('products', lazy='joined'), lazy='dynamic', cascade='all')

    def __init__(self, product_nr, name, shortdesc, longdesc, price, featured=True):
        self.product_nr = product_nr
        self.name = name
        self.shortdesc = shortdesc
        self.longdesc = longdesc
        # self.category_id = category_id
        self.featured = featured
        self.price = price

    def __repr__(self):
        return '<Products - {}>'.format(self.product_nr, self.name, self.shortdesc, self.longdesc, self.category_id,
                                        self.price)


class Images(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    thumbnail = db.Column(db.LargeBinary)
    image = db.Column(db.LargeBinary)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __init__(self, image, product_id):
        self.image = image
        self.product_id = product_id

    def __repr__(self):
        return '<Image  -{}'.format(self.image, self.product_id)


class Categories(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


# should be many to many relationship/ many Products can have many Tags.
class Tags(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


class Viewed(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ip = db.Column(db.Integer)
    viewed_on = db.Column(db.DateTime(), default=datetime.utcnow)
    browser = db.Column(db.Text)
    system = db.Column(db.Text)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    page_viewed = db.Column(db.Integer, db.ForeignKey('products.id'))


class Users(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    upqdated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow())