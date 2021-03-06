__author__ = 'justus'

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.compress import Compress


app = Flask(__name__, static_path='')
Compress(app)


app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

from app import view
from app.admin.view import mod as admin
from app.store.view import mod as store

app.register_blueprint(admin)
app.register_blueprint(store)
