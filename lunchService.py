import dao;

def findById(lunch_id):
    dao.getCursor().execute("""SELECT * FROM lunch WHERE lunch_id = ?""", lunch_id)

def add(id, time, owner_id, place, description):
    dao.getCursor().execute("""INSERT INTO lunch (id, time, owner_id, place, description) VALUES (?, ?, ?, ?)""", (id, time, owner_id, place, description))
    dao.get_connection().commit()

def joinLunch(user_id, lunch_id):
    result = []
    result.append(findById(lunch_id))


    dao.getCursor().execute("""INSERT INTO lunch (id, time, owner_id, place, description) VALUES (?, ?, ?, ?)""",
                            (id, time, owner_id, place, description))
    dao.get_connection().commit()

