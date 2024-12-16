import sqlite3

connection = sqlite3.connect('Products.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')


# создаём таблицу Products, если она ещё не создана при помощи SQL-запроса
def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    prod = cursor.fetchone()
    if prod is None:
        for i in range(1, 5):
            cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                           (f'Продукт{i}', f'Описание{i}', f'{i * 100}'))
            connection.commit()  # сохраняем состояние


# которая возвращает все записи из таблицы Products
def get_all_product():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")

    return cursor.fetchall()


connection.commit()  # сохраняем состояние
connection.close()  # закрываем соединение
