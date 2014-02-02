import MySQLdb as mdb
import sys

class DBWrapper:
    dbcur = None

    def __init__(self):
        pass

    def connect(self):
        db = mdb.connect(host="127.0.0.1",
                             user="root",
                             passwd="",
                             db="PP")

        cur = db.cursor()
        return cur

    def exe(self, cmd):
        if not self.dbcur:
            self.dbcur = self.connect()
        try:
            self.dbcur.execute(cmd)
            ret = self.dbcur.fetchall()
            return ret
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if self.dbcur:
                self.dbcur.close()

    def select(self, cmd):
        return self.exe(cmd)

    def insert(self, cmd):
        return self.exe(cmd)

    def update(self, cmd):
        return self.exe(cmd)

# dp = DBWrapper()
# print dp.select("SELECT * FROM stocks")