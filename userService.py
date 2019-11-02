import dao;

def add(user_id, city, lunch_id):
    dao.getCursor().execute("""INSERT INTO users (user_id, city, lunch_id) VALUES (?, ?, ?)""", (user_id, city, lunch_id))
    dao.get_connection().commit()

def findById(userId):
    return dao.getCursor().execute("""SELECT * FROM users WHERE user_id = ?""", int(userId))