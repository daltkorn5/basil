# coding=utf-8

from .tables.table_base import Session, engine, Base
from .tables.transactions import Transaction
from .tables.categories import Category
import datetime


Base.metadata.create_all(engine)
session = Session()

categories = session.query(Category).all()
if len(categories) == 0:
    test_category = Category("Test Category")
    session.add(test_category)
    session.commit()
    session.close()

    categories = session.query(Category).all()

transactions = session.query(Transaction).all()
if len(transactions) == 0:
    test_transaction = Transaction(datetime.date(2019,4,1), 20.00, 1, "Test Transaction", "daltkorn")
    session.add(test_transaction)
    session.commit()
    session.close()

    transactions = session.query(Transaction).all()

print('Transactions!')
for t in transactions:
    print(f"{t.transaction_id}: {t.description} for ${t.amount} on {t.transaction_date}")

print('Categories!')
for c in categories:
    print(f"{c.category_id}: {c.name}")
