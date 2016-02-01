__author__ = 'justus'

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_path='')

app.config.from_object(os.environ['APP_CONFIG'])

db = SQLAlchemy(app)

from app import view
