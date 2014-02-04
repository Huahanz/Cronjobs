import MySQLdb


class DBWrapper:
    dbcur = None

    def __init__(self):
        pass

    def connect(self):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="1234",
                             db="stock")

        cur = db.cursor()
        return cur

    def exe(self, cmd):
        if not self.dbcur:
            self.dbcur = self.connect()
        self.dbcur.execute(cmd)
        return self.dbcur.fetchall()

    def select(self, cmd):
        return self.exe(cmd)

    def insert(self, cmd):
        return self.exe(cmd)

    def update(self, cmd):
        return self.exe(cmd)

