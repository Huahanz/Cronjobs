from Reminder.Models.nasdaqstock import NasdaqStock
from Reminder.Models.dbmodel import DBModel


class NasdaqStockModel(DBModel):
    table_name = 'stocks'
    schema = {'symbol':'string', 'pattern':'string', 'min':'int', 'max':'int'}

    def __init__(self):
        DBModel.__init__(self, self.table_name)

    def get(self, id):
        return DBModel.get(self,id)

    def wrap_to_obj(self, data):
        print 'CORRECT '
        if len (data) != len(self.schema):
            print 'invalid data format'
            return None
        return NasdaqStock(data.symbol, data.pattern, data.min, data.max)

tm = NasdaqStockModel()
print tm.get_all()