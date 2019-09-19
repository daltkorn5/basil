# coding=utf-8

from flask import Blueprint, jsonify, request
from src.tables.table_base import Session
from src.tables.description_category_xref import DescriptionCategoryXref, DescriptionCategoryXrefSchema
from src.tables.categories import Category
from src.tables.transactions import Transaction

xref_blueprint = Blueprint('xref', __name__, url_prefix = '/xref')

@xref_blueprint.route('/get_all')
def get_categories():

    return jsonify(DescriptionCategoryXref.get_all())

@xref_blueprint.route('/no_category')
def get_where_category_is_null():

    return jsonify(DescriptionCategoryXref.where({"category_id": None}))

@xref_blueprint.route('/set_category/<category_id>', methods = ['POST'])
def set_category(category_id):

    category = Category.get(category_id)
    if category is None:
        return jsonify({"ERROR": f"cateogory_id {category_id} does not exist"}), 201

    posted_description = DescriptionCategoryXrefSchema(only = ("description",)).load(request.get_json())
    description = posted_description.data['description']

    xref = DescriptionCategoryXref.get((description,))
    if xref is None:
        return jsonify({"ERROR": f"description '{description}' does not exist"})

    DescriptionCategoryXref.update(
        filter_params = {"description": description},
        update_params = {"category_id": category_id}
    )

    # maybe we want to check to see if only one row needs to be updated? This could be inefficient
    num_updates = Transaction.update(
        filter_params = {'description': description},
        update_params = {'category_id': category_id}
    )

    return jsonify({"SUCCESS": f"{num_updates} transactions updated"}), 201
