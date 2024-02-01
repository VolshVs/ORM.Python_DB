from time import sleep

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


class FindPublisher:
    '''Класс по работе с БД.'''

    data_dict = {
        1: 'O’Reilly',
        2: 'No starch press',
        3: 'Microsoft Press',
        4: 'Pearson'
    }

    def find(number: int):
        '''Функция ищет данные из БД по издательству.'''
        publisher_ = FindPublisher.data_dict[number]
        Session = sessionmaker(bind=engine)
        session = Session()
        result_ = session.query(
            Publisher,
            Book,
            Stock,
            Sale,
            Shop
        ).join(
            Book,
            Publisher.id == Book.id_publisher
        ).join(
            Stock,
            Book.id == Stock.id_book
        ).join(
            Sale,
            Stock.id == Sale.id_stock
        ).join(
            Shop,
            Stock.id_shop == Shop.id
        ).filter(Publisher.name == publisher_)
        for publisher, book, stok, sale, shop in result_:
            print(
                f'{publisher.name} | Название книги: {book.title} '
                f'| название магазина: {shop.name} '
                f'| стоимость покупки: {sale.price} '
                f'| дата покупки: {sale.date_sale}'
            )
        session.close()

    def check(number: str) -> int:
        '''Функция проверяет правильность введения заданных значений.'''
        try:
            a = str(number)
            b = int(a)
        except (TypeError, ValueError):
            return print('Вы вышли за заданные рамки!')
        else:
            if 1 <= b <= 4:
                print("Запускаем процесс!\n")
                sleep(1)
                return FindPublisher.find(b)
            else:
                return print('Вы вышли за заданные рамки!')


if __name__ == '__main__':
    print('\nХотите найти нужное издательство?\n'
          'Введите число от 1 до 4, где:\n'
          '1 - O’Reilly;\n'
          '2 - No starch press;\n'
          '3 - Microsoft Press;\n'
          '4 - Pearson.\n'
          '')
    number = input('-> ')
    FindPublisher.check(number)
