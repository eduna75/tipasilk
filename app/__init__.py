__author__ = 'justus'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_path='')
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='postgresql://justus:73@Jul-7@127.0.0.1/tipasilk',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)

from app import view

# from the CRUD project
from app.admin.admin import admin
app.register_blueprint(admin)
