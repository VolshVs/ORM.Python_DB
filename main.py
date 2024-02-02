import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
import os

from models import create_tables, Publisher, Book, Shop, Stock, Sale
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('env/.env')
load_dotenv(dotenv_path=dotenv_path)
type_sql = os.getenv('TYPE_SQL')
login = os.getenv('LOGIN')
password = os.getenv('PASS')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')

DSN = (type_sql + '://' + login + ':' + password + '@' + host + ':' + port + '/' + db_name)
engine = sq.create_engine(DSN)
create_tables(engine)

with open('fixtures/tests_data.json', encoding="utf-8") as json_file:
    data = json.load(json_file)

for mod in data:
    model = str
    if mod['model'] == 'publisher':
        model = Publisher(
            id=mod['pk'],
            name=mod['fields']['name']
        )
    elif mod['model'] == 'book':
        model = Book(
            id=mod['pk'],
            title=mod['fields']['title'],
            id_publisher=mod['fields']['id_publisher']
        )
    elif mod['model'] == 'shop':
        model = Shop(
            id=mod['pk'],
            name=mod['fields']['name']
        )
    elif mod['model'] == 'stock':
        model = Stock(
            id=mod['pk'],
            id_book=mod['fields']['id_book'],
            id_shop=mod['fields']['id_shop'],
            count=mod['fields']['count']
        )
    elif mod['model'] == 'sale':
        model = Sale(
            id=mod['pk'],
            price=mod['fields']['price'],
            date_sale=mod['fields']['date_sale'],
            id_stock=mod['fields']['id_stock'], count=mod['fields']['count']
        )
    else:
        pass

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(model)
    session.commit()
    session.close()


def get_shops(user_input):
    Session = sessionmaker(bind=engine)
    dbsession = Session()
    session_body = dbsession.query(
        Book.title,
        Shop.name,
        Sale.price,
        Sale.date_sale
    ).select_from(
        Shop
    ).join(
        Stock, Stock.id_shop == Shop.id
    ).join(
        Book, Book.id == Stock.id_book
    ).join(
        Publisher, Publisher.id == Book.id_publisher
    ).join(
        Sale, Sale.id_stock == Stock.id
    )
    if user_input.isdigit():
        result_ = session_body.filter(Publisher.id == user_input).all()
    else:
        result_ = session_body.filter(Publisher.name == user_input).all()
    for title_, shop_name_, price_, date_sale_ in result_:
        print(
            f"{title_: <40} | {shop_name_: <10} | {price_: <8} | {date_sale_.strftime('%d-%m-%Y')}")
    session.close()


if __name__ == '__main__':
    user_input = input("Введите имя или айди публициста: ")
    get_shops(user_input)
