# coding=utf-8

from sqlalchemy import Column, Date, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .table_base import Base, TableBase
from .categories import Category

class Transaction(TableBase, Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key = True)
    transaction_date = Column(Date)
    amount = Column(Numeric)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    description = Column(String)
    created_by = Column(String)

    categories = relationship('Category')

    def __init__(self, transaction_date, amount, category_id, description, created_by):
        self.transaction_date = transaction_date
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.created_by = created_by
