__author__ = 'justus'

import os
_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = os.environ['SECRET_KEY']
    ADMIN_MENU = 'production'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL_TS']
    ADMIN_MENU = 'development'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ADMIN_MENU = 'production'