# coding=utf-8

from sqlalchemy import Column, Date, String, Integer, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .table_base import Base, TableBase, Session
from .categories import Category
from .description_category_xref import DescriptionCategoryXref
from marshmallow import Schema, fields

class TransactionSchema(Schema):
    transaction_id = fields.Integer()
    transaction_date = fields.Date()
    amount = fields.String() # Ideally would be decimal but decimal type isn't serializable
    category_id = fields.Integer()
    description = fields.String()
    created_by = fields.String()

class Transaction(TableBase, Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key = True)
    transaction_date = Column(Date)
    amount = Column(Numeric)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    description = Column(String)
    created_by = Column(String)

    schema = TransactionSchema

    __table_args__ = (UniqueConstraint("transaction_date", "amount", "description"),)

    def __init__(self, transaction_date, amount, description, created_by, category_id = None):
        self.transaction_date = transaction_date
        self.amount = amount
        self.description = description
        self.created_by = created_by
        self.category_id = self.lookup_category(description) if category_id is None else category_id

    def lookup_category(self, desc):
        """
        Check to see if we already have a mapping for the newly added transaction's description
        """
        xref = session.query(DescriptionCategoryXref).get(desc)
        if xref is not None:
            return xref.category_id

        return None
