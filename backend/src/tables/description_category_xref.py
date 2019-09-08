# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from .table_base import Base, TableBase
from marshmallow import Schema, fields

class DescriptionCategoryXrefSchema(Schema):
    category_id = fields.Integer()
    description = fields.String()

class DescriptionCategoryXref(TableBase, Base):
    __tablename__ = 'description_category_xref'
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    description = Column(String, primary_key = True)

    schema = DescriptionCategoryXrefSchema

    def __init__(self, category_id, description):
        self.category_id = category_id
        self.description = description
