#Сервис, предоставляющий CRUD методы по работе с таблицей Обед
#Service provides CRUD operation with table Lunch

# imports
import dao;

# functions
"""
    Возвращает информацию об обеде по идентфикатору
    - lunch_id - идентификатор обеда
    Return lunch information by lunch_id 
 """
def findById(lunch_id):
    param = int(lunch_id)
    result = dao.getCursor().execute("""SELECT id, time, owner_id, place, description FROM lunch WHERE id = ?""",
                                     [param]).fetchone()

    lunch = {
        'id': result[0], 'time': result[1], 'owner_id': result[2], 'place': result[3], 'description': result[4]
    }

    return lunch

def findByOwnerId(owner_id):
    param = int(owner_id)
    result = dao.getCursor().execute("""SELECT id, time, owner_id, place, description FROM lunch WHERE owner_id = ?""",
                                     [param]).fetchone()

    lunch = {
        'id': result[0], 'time': result[1], 'owner_id': result[2], 'place': result[3], 'description': result[4]
    }

    return lunch

"""
    Добавляет информацию об обеде
    - time - время обеда / lunch time
    - owner_id - создатель обеда / lunch owner
    Add information about lunch 
 """
def add(time, owner_id, place, description):
    dao.getCursor().execute("""INSERT INTO lunch (time, owner_id, place, description) VALUES (?, ?, ?, ?)""",
                            (time, int(owner_id), place, description))
    dao.get_connection().commit()

"""
    Удаляет информацию об обеде
    - lunch_id - идентификатор обеда
    Delete information about lunch by lunchId 
 """
def delete(lunchId):
    param = int(lunchId)
    dao.getCursor().execute("""DELETE FROM lunch WHERE id = ?""", [param])
    dao.get_connection().commit()


"""
    Возвращает список всех возможных вариантов обеда
    Return all lunch infos
 """
def getAll():
    fromDb = dao.getCursor().execute("""SELECT id, time, owner_id, place, description FROM lunch""").fetchmany()
    result = []

    for row in fromDb:
        lunch = {
            'id': row[0], 'time': row[1], 'owner_id': row[2], 'place': row[3], 'description': row[4]
        }
        result.append(lunch)

    return result


"""
    Возвращает список всех возможных вариантов обеда, доступных текущему пользователю
    - userId - текущий пользователь / active user
    Return available lunch infos for active user
 """
def getAllByUserId(userId):
    param = int(userId)
    fromDb = dao.getCursor().execute("""SELECT id, time, owner_id, place, description FROM lunch 
                                        JOIN users ON lunch.owner_id = users.user_id
                                        WHERE city in (SELECT city from users where user_id = ?)""",
                                     [param]).fetchmany()

    result = []

    for row in fromDb:
        lunch = {
            'id': row[0], 'time': row[1], 'owner_id': row[2], 'place': row[3], 'description': row[4]
        }
        result.append(lunch)

    return result

"""
    Возвращает информацию об обеде, на который зарегистрировался текущий пользователь
    - userId - текущий пользователь / active user
    Return lunch info booked by active user
 """
def getActiveByUserId(userId):
    param = int(userId)
    result = dao.getCursor().execute("""SELECT id, time, owner_id, place, description FROM lunch 
                                        JOIN users ON users.lunch_id = lunch.id
                                        WHERE users.user_id = ?""",
                                 [param]).fetchone()
    lunch = {
        'id': result[0], 'time': result[1], 'owner_id': result[2], 'place': result[3], 'description': result[4]
    }

    return lunch
