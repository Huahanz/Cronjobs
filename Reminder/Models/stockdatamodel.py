from Reminder.Models.StockData import StockData
from Reminder.Models.dbmodel import DBModel


class StockDataModel(DBModel):
    table_name = 'stockdata'
    #schema = {'id': 'int', 'symbol': 'string', 'price': 'float', 'vol': 'int'}
    schema = [
        ['id', 'int'],
        ['symbol', 'string'],
        ['price', 'float'],
        ['vol', 'int']
    ]

    def __init__(self):
        DBModel.__init__(self, self.table_name)

    def get(self, id, offset=None, limit=None):
        return DBModel.get(self, id)

    def save(self, obj):
        return DBModel.save(self, obj)

    def update(self, symbol, price, vol):
        id = self.generate_id(symbol)
        obj = StockData(id, symbol, price, vol)
        self.save(obj)

    def generate_id(self, symbol):
        id = 0
        for c in symbol:
            id += (ord(c) - 97)
            id *= 26
        return id

    def wrap_to_obj(self, data):
        if len(data) != len(self.schema):
            print 'invalid data format'
            return None
        return StockData(data[0], data[1], data[2], data[3])

    def get_price_by_symbol(self, symbol):
        id = self.generate_id(symbol)
        entry = self.get(id)
        if isinstance(entry, (list, tuple)):
            entry = entry[0]
        if entry:
            return entry.price
        else:
            return None

#sd = StockDataModel()
#print ''.join(sd.get(None)
#sx = StockData(1, 'yelp', 100, 100000)
#sd.save(sx)
#print ''.join(sd.get(None))
