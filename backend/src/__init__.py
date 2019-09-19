import os, datetime
from flask import Flask
from flask.json import JSONEncoder
from .tables.table_base import engine, Base, Session
from .tables.categories import Category
from .tables.transactions import Transaction
from .tables.description_category_xref import DescriptionCategoryXref

class CustomJSONEncoder(JSONEncoder):
    """
    Class to make it so that flask's jsonify function keeps dates and datetimes in
    iso format
    taken from https://stackoverflow.com/questions/43663552/keep-a-datetime-date-in-yyyy-mm-dd-format-when-using-flasks-jsonify
    """
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

def create_app():
    Base.metadata.create_all(engine)
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

    from .routes.transactions import transaction_blueprint
    app.register_blueprint(transaction_blueprint)

    from .routes.categories import category_blueprint
    app.register_blueprint(category_blueprint)

    from .routes.description_category_xref import xref_blueprint
    app.register_blueprint(xref_blueprint)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
