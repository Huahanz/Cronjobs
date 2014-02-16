import MySQLdb


class DBWrapper:
    def __init__(self):
        pass

    def exe(self, cmd):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="1234",
                             db="stock")
        dbcur = db.cursor()
        dbcur.execute(cmd)
        ret = dbcur.fetchall()
        db.close()
	return ret

    def select(self, cmd):
        return self.exe(cmd)

    def commit(self, cmd):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="1234",
                             db="stock")
        dbcur = db.cursor()
        dbcur.execute(cmd)
        db.commit()
        db.rollback()
        db.close()

    def insert(self, cmd):
        return self.commit(cmd)

    def update(self, cmd):
        return self.commit(cmd)

