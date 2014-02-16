import MySQLdb

class DBWrapper:
    dbcur = None
    db = None

    def __init__(self):
        pass

    def connect(self):
        self.db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="1234",
                             db="stock")
        self.dbcur = self.db.cursor()

    def exe(self, cmd):
        try:
            self.connect()
            self.dbcur.execute(cmd)
            return self.dbcur.fetchall()
        finally:
            self.db.close()

    def select(self, cmd):
        return self.exe(cmd)

    def commit(self, cmd):
        try:
            self.connect()
            self.dbcur.execute(cmd)
            self.db.commit()
        except:
            self.db.rollback()

    def insert(self, cmd):
        return self.commit(cmd)

    def update(self, cmd):
        return self.commit(cmd)

