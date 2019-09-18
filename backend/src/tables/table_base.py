# coding=utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# get the db connection info from the .pgpass file
homedir = os.getenv("HOME")
with open(f"{homedir}/.pgpass", 'r') as fp:
    config = fp.read().split(":")

db_url      = config[0] + ":" + config[1]
db_name     = config[2]
db_user     = config[3]
db_password = config[4]

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind = engine)

Base = declarative_base()

class TableBase():

    def __init__(self):
        pass

    # Doing session.query... over and over was going to be too wordy
    # so here are some class methods that make it a bit shorter to initiate database commands via the ORMs
    @classmethod
    def get(cls, primary_key):
        """Get a single record in the table as specified by the primary key"""
        session = Session()
        result = session.query(cls).get(*primary_key)
        session.close()
        return result

    @classmethod
    def get_all(cls):
        """Get all records in the table"""
        session = Session()
        objects = session.query(cls).all()
        objects = cls.schema(many = True).dump(objects).data
        session.close()

        return objects

    @classmethod
    def where_unique(cls, filter_params):
        """Get the unique record specified by the filter_params dict"""
        session = Session()
        result = session.query(cls).filter_by(**filter_params).one()
        session.close()
        return result

    @classmethod
    def where(cls, filter_params):
        """Get all records as specified by the filter_params dict"""
        session = Session()
        result = session.query(cls).filter_by(**filter_params).all()
        session.close()
        return result

    @classmethod
    def insert(cls, posted_data):
        """Add new records to the database"""
        session = Session()

        try:
            new_data = [cls(**data) for data in posted_data]
            session.add_all(new_data)
            session.commit()
            ret_value = cls.schema(many = True).dump(new_data).data
        except IntegrityError:
            session.rollback()
            ret_value = {"ERROR": "record already exists"}

        session.close()
        return ret_value

    @classmethod
    def update(cls, filter_params, update_params):
        """
        Class method to bulk update records.
        filter_params is the dict used to specify which records you want to update
        update_params is the dict used to specify how to update them

        For example:
            Table.update(
                filter_params = {'col1': val1},
                update_params = {'col2': val2}
            )
            is equivalent to the SQL Statement:
                update table set col2 = val2 where col1 = val1;
        """
        session = Session()
        num_updates = session.query(cls).filter_by(**filter_params).update(update_params)
        session.commit()
        session.close()

        return num_updates
