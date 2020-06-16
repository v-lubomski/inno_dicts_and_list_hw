"""Скрипт принимае json-файл, проверяет его на валидность и в случае успешной проверки записывает данные в БД."""

from json import load
from jsonschema import validate
from jsonschema import exceptions
import sqlite3
from typing import Any

JSON_FILENAME = 'example.json'
JSON_SCHEMA_FILENAME = 'json.schema'
DB_FILENAME = 'database.db'

# создаём базу данных и таблицы
conn = sqlite3.connect(DB_FILENAME)
cursor = conn.cursor()
cursor.executescript(
    'CREATE TABLE IF NOT EXISTS goods('
    'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
    'name VARCHAR NOT NULL,'
    'package_height FLOAT NOT NULL,'
    'package_width FLOAT NOT NULL);'
    ''
    'CREATE TABLE IF NOT EXISTS shops_goods('
    'id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT,'
    'id_good INTEGER NOT NULL,'
    'location VARCHAR NOT NULL,'
    'amount INTEGER NOT NULL,'
    'FOREIGN KEY (id_good) REFERENCES goods (id));'
)

with open(JSON_FILENAME, encoding='utf-8') as file:
    json_data = load(file)

with open(JSON_SCHEMA_FILENAME) as file:
    json_schema = load(file)


def add_data_to_db(data: dict, schema: dict) -> None:
    """Функция валидации и добавления данных в БД."""
    def validate_json() -> Any:
        try:
            validate(instance=data, schema=schema)
        except exceptions.ValidationError as err:
            return err

    def add_data() -> None:
        # записываем данные в первую таблицу
        id_good = data['id']
        name_good = data['name']
        package_height = data['package_params']['height']
        package_width = data['package_params']['width']
        cursor.execute(
            'INSERT OR REPLACE INTO goods(id, name, package_height, package_width) VALUES (?,?,?,?)',
            (id_good, name_good, package_height, package_width))
        conn.commit()

        # записываем данные во вторую таблицу
        shop_goods = data['location_and_quantity']
        for shop in shop_goods:
            check = cursor.execute(
                'SELECT id FROM shops_goods WHERE id_good=(?) AND location=(?)', (id_good, shop['location'])
            ).fetchone()
            if check:
                cursor.execute(
                    'UPDATE shops_goods SET amount=(?) WHERE id_good=(?) AND location=(?)',
                    (shop['amount'], id_good, shop['location']))
            else:
                cursor.execute(
                    'INSERT INTO shops_goods(id_good, location, amount) VALUES (?,?,?)',
                    (id_good, shop['location'], shop['amount']))
            conn.commit()

    # если валидация успешна - вызываем функцию записи в БД
    is_error = validate_json()
    if not is_error:
        add_data()
        print('Данные успешно добавлены')
    else:
        print(f'Данные не валидны, добавление в БД прервано\n\n {is_error}')


add_data_to_db(json_data, json_schema)
