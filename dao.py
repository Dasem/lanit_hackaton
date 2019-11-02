import sqlite3
from sqlite3 import Error

conn = None
cursor = None


def get_connection():
    global conn
    if conn is not None:
        return conn
    try:
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        return conn
    except Error as e:
        print(e)


def getCursor():
    global cursor
    if cursor is not None:
        return cursor
    return get_connection().cursor()


def close_connection(connection):
    connection.close()


def initDbTables():
    getCursor().execute(
        """CREATE TABLE IF NOT EXISTS lunch (id integer PRIMARY KEY, time VARCHAR, owner_id integer, place VARCHAR, description VARCHAR );""")
    getCursor().execute(
        """CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY, city VARCHAR, lunch_id integer, CONSTRAINT fkLunch FOREIGN KEY (lunch_id) REFERENCES lunch (id));""")
