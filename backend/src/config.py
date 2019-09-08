import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'dev'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'localhost:5432'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
