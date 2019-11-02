#Класс содержит конфигурации по работе с БД
#Contains db configuration

# imports
import sqlite3
from sqlite3 import Error

# Variables with simple values
conn = None
cursor = None

# functions
"""
    Возвращает текущий или создаем новый коннект к БД
    Return active or new db connection
 """
def get_connection():
    global conn
    if conn is not None:
        return conn
    try:
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        return conn
    except Error as e:
        print(e)


""" 
    Возвращает курсор текущего коннекта
    Return a cursor for the active connection 
"""
def getCursor():
    global cursor
    if cursor is not None:
        return cursor
    return get_connection().cursor()


""" 
   Закрывает коннект
   Close the connection
"""
def close_connection(connection):
    connection.close()


""" 
   Создает таблицы в БД
   Create database tables
"""
def initDbTables():
    getCursor().execute(
        """CREATE TABLE IF NOT EXISTS lunch (id integer PRIMARY KEY AUTOINCREMENT, time VARCHAR, owner_id integer, place VARCHAR, description VARCHAR );""")
    getCursor().execute(
        """CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY, city VARCHAR, lunch_id integer, CONSTRAINT fkLunch FOREIGN KEY (lunch_id) REFERENCES lunch (id));""")
