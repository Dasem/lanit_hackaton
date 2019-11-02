#Сервис, предоставляющий CRUD методы по работе с таблицей Пользователь
#Service provides CRUD operation with table Users

# imports
import dao;


# functions
"""
    Добавляет информацию об пользователе
    - user_id - идентфикатор пользователя
    - city - город нахождения пользователя
    - lunch_id - идентификатор, выбранного обеда
    Add information about user
 """
def add(user_id, city, lunch_id):
    dao.getCursor().execute("""INSERT INTO users (user_id, city, lunch_id) VALUES (?, ?, ?)""",
                            (user_id, city, lunch_id))
    dao.get_connection().commit()


def findById(userId):
    result = dao.getCursor().execute("""SELECT user_id, city, lunch_id FROM users WHERE user_id = ?""",
                                     [int(userId)]).fetchone()
    if result is None:
        return None
    user = {'user_id': result[0], 'city': result[1], 'lunch_id': result[2]}
    return user


def joinLunch(user_id, lunch_id):
    dao.getCursor().execute("""UPDATE users SET lunch_id = ? WHERE user_id = ?""", (lunch_id, user_id))
    dao.get_connection().commit()


def leaveLunch(user_id):
    # TODO добавить проверку не пытаемся ли мы выйти из собственного обеда
    dao.getCursor().execute("""UPDATE users SET lunch_id = ? WHERE user_id = ?""", (-1, user_id))
    dao.get_connection().commit()


# Возвращает массив массивов
def getAllByLunchId(lunchId):
    param = int(lunchId)
    result = dao.getCursor().execute("""SELECT user_id FROM users WHERE lunch_id = ?""",
                                     [param]).fetchall()
    return result
