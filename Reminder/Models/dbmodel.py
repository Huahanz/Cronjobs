from Reminder.DB.dbwrapper import DBWrapper


class DBModel:
    table_name = None
    dbconnection = None
    def __init__(self, table_name):
        pass

    def get(self, id, offset=None, limit=None):
        cmd = 'SELECT * FROM ' + self.table_name
        if id:
            cmd += ' WHERE id = ' + id
        if not DBModel.dbconnection:
            DBModel.dbconnection = DBWrapper()
            DBModel.dbconnection.connect()
        data = DBModel.dbconnection.select(cmd)
        print 'data : ', data
	if type(data) is tuple:
	    ret = []
	    for entry in data:
		ret.append(self.wrap_to_obj(entry))
	    return ret
	else:
            return self.wrap_to_obj(data)

    def set(self, id, update):
        cmd = 'UPDATE ' + self.table_name + ' Set '
        for k, v in update.iteritems():
            cmd += k + ' = \'' + v + '\', '
        cmd += ' WHERE id = ' + id
        print 'update : ', cmd
        if not DBModel.dbconnection:
            DBModel.dbconnection = DBWrapper()
            DBModel.dbconnection.connect()
        DBModel.dbconnection.update(cmd)
        return

    def wrap_to_obj(self, data):
        print ' error : in parent '
        pass

    def get_all(self):
        return self.get(None)
