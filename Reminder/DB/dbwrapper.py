import MySQLdb
from random import choice
from random import randrange

class DBWrapper:
    dbcurs = []
    dbs = []

    def __init__(self):
	self.connet_by_pool(100)
        pass

    def connect(self):
       	print '@@ getting db connection'
        db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="1234",
                                  db="stock")
        self.dbs.append(db)
        self.dbcurs.append(db.cursor())
        return True

    def connet_by_pool(self, num):
        for i in range(0, num):
            self.connect()

    def exe(self, cmd):
        if not self.dbcurs:
            self.connect()
        print '@@ exe ' + cmd
        dbcur = choice(self.dbcurs)
        dbcur.execute(cmd)
        return dbcur.fetchall()

    def select(self, cmd):
        return self.exe(cmd)

    def commit(self, cmd):
        if not self.dbcurs:
            self.connect()
        try:
            ix = randrange(0, len(self.dbcurs))
            dbcur = self.dbcurs[ix]
            db = self.dbs[ix]
            dbcur.execute(cmd)
            db.commit()
        except:
            db.rollback()

    def insert(self, cmd):
        return self.commit(cmd)

    def update(self, cmd):
        return self.commit(cmd)

