# coding=utf-8

from flask import Blueprint, jsonify, request
from sqlalchemy import func, Date
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

@transaction_blueprint.route('/set_category/<category_id>', methods = ['POST'])
def set_category(category_id):

    category = Category.get(category_id)
    if category is None:
        return jsonify({"ERROR": f"cateogory_id {category_id} does not exist"}), 201

    posted_transaction = TransactionSchema(only = ("transaction_id",)).load(request.get_json())

    id = posted_transaction.data['transaction_id']

    transaction = Transaction.get(id)
    if transaction is None:
        return jsonify({"ERROR": f"transaction_id {transaction_id} does not exist"}), 201

    update_xref(transaction.description, category_id)

    # maybe we want to check to see if only one row needs to be updated? This could be inefficient
    num_updates = Transaction.update(
        filter_params = {'description': transaction.description},
        update_params = {'category_id': category_id}
    )

    return jsonify({"SUCCESS": f"{num_updates} transactions updated"}), 201

@transaction_blueprint.route('/aggregate')
def aggregate_transactions():

    session = Session()

    aggregation = session.query(
        label('month', func.cast(func.date_trunc('month', Transaction.transaction_date), Date)),
        label('category', Category.name),
        label('sum', func.text(func.sum(Transaction.amount))) # has to be text because Decimal isn't json serializable :(
    ).join(Category).group_by(
        func.cast(func.date_trunc('month', Transaction.transaction_date), Date),
        Category.name
    ).all()

    aggregation = [row._asdict() for row in aggregation]

    session.close()
    return jsonify(aggregation), 201

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
