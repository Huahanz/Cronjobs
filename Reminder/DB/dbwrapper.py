import MySQLdb


class DBWrapper:
    dbcur = None

    def __init__(self):
        pass

    def connect(self):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="",
                             db="PP")

        cur = db.cursor()
        return cur

    def exe(self, cmd):
        if not self.dbcur:
            self.dbcur = self.connect()
        self.dbcur.execute(cmd)
        return self.dbcur.fetchall()

    def select(self, cmd):
        self.exe(cmd)

    def insert(self, cmd):
        self.exe(cmd)

    def update(self, cmd):
        self.exe(cmd)

dp = DBWrapper()
dp.select("SELECT * FROM balls")