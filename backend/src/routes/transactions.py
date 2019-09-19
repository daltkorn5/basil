# coding=utf-8

import datetime, calendar
from flask import Blueprint, jsonify, request
from sqlalchemy import func, Date, case
from sqlalchemy.sql import label
from src.tables.table_base import Session
from src.tables.transactions import Transaction, TransactionSchema
from src.tables.categories import Category
from src.tables.description_category_xref import DescriptionCategoryXref

transaction_blueprint = Blueprint('transactions', __name__, url_prefix = '/transaction')

@transaction_blueprint.route('/get_all')
def get_transactions():

    return jsonify(Transaction.get_all())

@transaction_blueprint.route('/add', methods = ['POST'])
def add_transaction():

    posted_transaction = TransactionSchema(
        many = True,
        only = ('transaction_date', 'amount', 'description', 'created_by', 'category_id'),
        partial = False # We want transactions to be added even if cateogory_id isn't specified
    ).load(request.get_json())

    transaction = Transaction.insert(posted_transaction.data)

    return jsonify(transaction), 201

@transaction_blueprint.route('/aggregate')
def aggregate_transactions():

    session = Session()

    aggregation = session.query(*get_select()).join(Category, isouter = True).group_by(*get_group_by()).all()

    aggregation = [row._asdict() for row in aggregation]

    session.close()
    return jsonify(aggregation), 201

@transaction_blueprint.route('/aggregate/<month>')
def aggregate_transactions_for_month(month):

    first_of_month, last_of_month = get_month_boundaries(month)

    session = Session()

    aggregation = session.query(*get_select()).join(Category, isouter = True).filter(
        Transaction.transaction_date >= first_of_month,
        Transaction.transaction_date <= last_of_month
    ).group_by(*get_group_by()).all()

    aggregation = [row._asdict() for row in aggregation]

    session.close()
    return jsonify(aggregation), 201

def get_month_boundaries(month_str):

    d = datetime.datetime.strptime(month_str, "%Y-%m-%d").date()
    month_range = calendar.monthrange(d.year, d.month)
    first_day = d.replace(day = 1)
    last_day = d.replace(day = month_range[1])

    return first_day, last_day

def update_xref(description, category_id):
    """
    If the transaction's description isn't in the description_category_xref table,
    we want to create a new record mapping the description to the supplied category_id

    If the transaction's description is in the description_category_xref,
    but the associated category_id is not equal to the supplied category_id,
    we want to update the mapping
    """
    xref = DescriptionCategoryXref.get(description)
    if xref is None:
        DescriptionCategoryXref.insert({'description': description, 'category_id': category_id})
    elif xref.category_id != category_id:
        DescriptionCategoryXref.update(
            filter_params = {'description': description},
            update_params = {'category_id': category_id}
        )

def get_select():
    return (
        label('month', func.cast(func.date_trunc('month', Transaction.transaction_date), Date)),
        label('category', get_case_statement()),
        label('sum', func.text(func.sum(Transaction.amount))) # has to be text because Decimal isn't json serializable :(
    )

def get_case_statement():
    return case(
        [
            (Category.name == None, 'None'),
        ],
        else_ = Category.name
    )

def get_group_by():
    return (
        func.cast(func.date_trunc('month', Transaction.transaction_date), Date),
        Category.name
    )
