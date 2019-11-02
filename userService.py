import dao;

def add(user_id, city, lunch_id):
    dao.getCursor().execute("""INSERT INTO users (user_id, city, lunch_id) VALUES (?, ?, ?)""",
                            (user_id, city, lunch_id))
    dao.get_connection().commit()


def findById(userId):
    result = dao.getCursor().execute("""SELECT user_id, city, lunch_id FROM users WHERE user_id = ?""",
                                     [int(userId)]).fetchone()
    user = {'user_id': result[0], 'city': result[1], 'lunch_id': result[2]}
    return user
