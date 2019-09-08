# coding=utf-8

from flask import Blueprint, jsonify, request
from src.tables.table_base import Session
from src.tables.categories import Category, CategorySchema

category_blueprint = Blueprint('categories', __name__, url_prefix = '/category')

@category_blueprint.route('/get_all')
def get_categories():

    return jsonify(Category.get_all())

@category_blueprint.route('/add', methods = ['POST'])
def add_category():
    posted_category = CategorySchema(only = ("name",)).load(request.get_json())

    category = Category.insert(posted_category.data)

    return jsonify(category), 201
