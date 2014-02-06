from Reminder.Models.NasdaqStock import NasdaqStock
from Reminder.Models.dbmodel import DBModel


class NasdaqStockModel(DBModel):
    table_name = 'stocks'
    schema = {'id': 'int', 'symbol': 'string', 'pattern': 'string', 'min': 'int', 'max': 'int'}

    def __init__(self):
        DBModel.__init__(self, self.table_name)

    def get(self, id, offset=None, limit=None):
        return DBModel.get(self, id)

    def wrap_to_obj(self, data):
        if len(data) != len(self.schema):
            print 'invalid data format'
            return None
        return NasdaqStock(data[0], data[1], data[2], data[3], data[4])
