from Reminder.Models.NasdaqStock import NasdaqStock
from Reminder.Models.dbmodel import DBModel


class NasdaqStockModel(DBModel):
    table_name = 'stocks'
    schema = [
        ['id', 'int'],
        ['symbol', 'string'],
        ['pattern', 'string'],
        ['min', 'int'],
        ['max', 'int'],
    ]

    def __init__(self):
        DBModel.__init__(self, True)

    def get(self, id, offset=None, limit=None):
        return DBModel.get(self, id)

    def get_by_symbol(self, symbol):
        id = self.generate_id(symbol)
        return self.get(id)

    def wrap_to_obj(self, data):
        if len(data) != len(self.schema):
            print 'invalid data format'
            return None
        return NasdaqStock(data[0], data[1], data[2], data[3], data[4])

    def generate_id(self, symbol):
        id = 0
        for c in symbol:
            id += (ord(c) - 97)
            id *= 26
        return id

    def reformat(self, stock_set):
        print 'reformating'
        if not isinstance(stock_set, basestring):
            for stock_obj in stock_set:
                self.__reformat(stock_obj)
        else:
            self.__reformat(stock_set)

    def __reformat(self, stock_obj):
        self.delete(stock_obj.id)
        stock_obj.symbol = stock_obj.symbol.upper()
        stock_obj.id = self.generate_id(stock_obj.symbol)
        return self.save(stock_obj)
