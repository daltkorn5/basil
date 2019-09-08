import os
from flask import Flask
from .tables.table_base import engine, Base, Session
from .tables.categories import Category
from .tables.transactions import Transaction
from .tables.description_category_xref import DescriptionCategoryXref

def create_app():
    Base.metadata.create_all(engine)
    app = Flask(__name__)

    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

    from .routes.transactions import transaction_blueprint
    app.register_blueprint(transaction_blueprint)

    from .routes.categories import category_blueprint
    app.register_blueprint(category_blueprint)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
