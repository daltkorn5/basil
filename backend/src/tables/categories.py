# coding=utf-8

from sqlalchemy import Column, String, Integer
from .table_base import Base, TableBase

class Category(TableBase, Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key = True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
