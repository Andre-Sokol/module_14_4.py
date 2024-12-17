import sqlite3

def initiate_db():
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


    for i in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (f'Продукт{i}', f'Описание{i}', f'{i * 100}'))
        connection.commit()  # сохраняем состояние
    connection.close()  # закрываем соединение


# которая возвращает все записи из таблицы Products
def get_all_product():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")

    return cursor.fetchall()




