import dao;


def findById(lunch_id):
    result = dao.getCursor().execute("""SELECT id, time, owner_id, place, description FROM lunch WHERE id = ?""",
                                     lunch_id).fetchone()
    lunch = {
        'id': result[0], 'time': result[1], 'owner_id': result[2], 'place': result[3], 'description': result[4]
    }

    return lunch


def add(time, owner_id, place, description):
    dao.getCursor().execute("""INSERT INTO lunch (time, owner_id, place, description) VALUES (?, ?, ?, ?)""",
                            (time, owner_id, place, description))
    dao.get_connection().commit()


def delete(lunchId):
    param = int(lunchId)
    dao.getCursor().execute("""DELETE FROM lunch WHERE id = ?""", [param])
    dao.get_connection().commit()


def getAllByUserId(userId):
    param = userId
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
