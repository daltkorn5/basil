# coding=utf-8

from datetime import datetime
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url      = 'localhost:5432'
db_name     = 'basil'
db_user     = 'postgres'
db_password = 'basil'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class TableBase():

    def __init__(self):
        pass
