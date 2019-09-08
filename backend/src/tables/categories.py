# coding=utf-8

from sqlalchemy import Column, String, Integer
from .table_base import Base, TableBase
from marshmallow import Schema, fields

class CategorySchema(Schema):
    category_id = fields.Integer()
    name = fields.String()

class Category(TableBase, Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key = True)
    name = Column(String)

    schema = CategorySchema

    def __init__(self, name):
        self.name = name
