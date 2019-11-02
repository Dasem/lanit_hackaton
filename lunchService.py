import dao;

def findById(lunch_id):
    dao.getCursor().execute("""SELECT * FROM lunch WHERE lunch_id = ?""", lunch_id)

def add(id, time, owner_id, place, description):
    dao.getCursor().execute("""INSERT INTO lunch (id, time, owner_id, place, description) VALUES (?, ?, ?, ?)""", (id, time, owner_id, place, description))
    dao.get_connection().commit()

def delete(lunchId):
    param = int(lunchId)
    dao.getCursor().execute("""DELETE FROM lunch WHERE id = ?""", [param])
    dao.get_connection().commit()

