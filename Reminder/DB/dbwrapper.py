import MySQLdb


class DBWrapper:
    dbcur = None
    db = None

    def __init__(self):
        pass

    def connect(self):
        print '@@ getting db connection'
        self.db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="1234",
                                  db="stock")

        self.dbcur = self.db.cursor()
        return True

    def exe(self, cmd):
        if not self.dbcur:
            self.connect()
        print '@@ exe ' + cmd
        self.dbcur.execute(cmd)
        return self.dbcur.fetchall()

    def select(self, cmd):
        return self.exe(cmd)

    def commit(self, cmd):
        if not self.dbcur:
            self.dbcur = self.connect()
        try:
            self.dbcur.execute(cmd)
            self.db.commit()
        except:
            self.db.rollback()

    def insert(self, cmd):
        return self.commit(cmd)

    def update(self, cmd):
        return self.commit(cmd)

