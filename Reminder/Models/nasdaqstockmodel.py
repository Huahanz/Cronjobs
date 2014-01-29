from Reminder.Models.nasdaqstock import NasdaqStock
from Reminder.Models.dbmodel import DBModel

class NasdaqStockModel(DBModel):
    table_name = 'stocks'

    def __init__(self):
        DBModel.__init__(self, self.table_name)

    def get(self, id):
        return DBModel.get(self,id)

    def wrap_to_obj(self, data):
        obj = NasdaqStock()
        print 'CORRECT '
        obj.symbol = data.symbol