from Reminder.DB.dbwrapper import DBWrapper


class DBModel:
    table_name = None
    dbconnection = None

    def __init__(self, table_name):
        pass

    def get(self, id, offset=None, limit=None):
        cmd = 'SELECT * FROM ' + self.table_name
        if id:
            cmd += ' WHERE id = ' + str(id)
        if not DBModel.dbconnection:
            DBModel.dbconnection = DBWrapper()
            DBModel.dbconnection.connect()
        data = DBModel.dbconnection.select(cmd)
        # print 'data : ', data
        if type(data) is tuple:
            ret = []
            for entry in data:
                ret.append(self.wrap_to_obj(entry))
            return ret
        else:
            return self.wrap_to_obj(data)

    def set(self, obj):
        data = self.wrap_to_sql_update_data(obj)
        if data:
            cmd = 'UPDATE ' + self.table_name + ' Set '
            cmd += data
            cmd += ' WHERE id = ' + str(obj.id) + ';'
            #print 'update : ', cmd
        if not DBModel.dbconnection:
            DBModel.dbconnection = DBWrapper()
            DBModel.dbconnection.connect()
        DBModel.dbconnection.update(cmd)
        return

    def add(self, obj):
        data = self.wrap_to_sql_insert_data(obj)
        if data:
            cmd = 'INSERT INTO ' + self.table_name + ' VALUES ('
            cmd += data
            cmd += ');'
            #print '@@ ' ,  cmd
            if not DBModel.dbconnection:
                DBModel.dbconnection = DBWrapper()
                DBModel.dbconnection.connect()
            ret = DBModel.dbconnection.insert(cmd)
            print '#', ret
            return ret
        return None

    def save(self, obj):
        if not obj.id:
            return self.add(obj)
        else:
            is_in_db = self.get(obj.id)
            if not is_in_db:
                return self.add(obj)
            else:
                return self.set(obj)

    def get_id():
        pass

    def wrap_to_obj(self, data):
        pass

    def wrap_to_sql_insert_data(self, obj):
        sql_cmd = ''
        for col in self.schema:
            val = getattr(obj, col[0])
            sql_cmd += ' \'' + str(val) + '\', '
        if sql_cmd:
            return sql_cmd[:-2]
        return sql_cmd

    def wrap_to_sql_update_data(self, obj):
        sql_cmd = ''
        for col in self.schema:
            if col[0] == 'id':
                continue
            val = getattr(obj, col[0])
            sql_cmd += col[0] + ' =  \'' + str(val) + '\', '
        if sql_cmd:
            return sql_cmd[:-2]
        return sql_cmd

    def get_all(self):
        return self.get(None)
