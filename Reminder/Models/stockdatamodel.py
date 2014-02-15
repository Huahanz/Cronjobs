from Reminder.Models.StockData import StockData
from Reminder.Models.dbmodel import DBModel
import json

class StockDataModel(DBModel):
    table_name = 'stockdata'
    #schema = {'id': 'int', 'symbol': 'string', 'price': 'float', 'vol': 'int'}
    schema = [
        ['id', 'int'],
        ['symbol', 'string'],
        ['price', 'float'],
        ['vol', 'int'],
        ['price_data', 'string'],
    ]

    json_field = 'price_data'

    def __init__(self):
        DBModel.__init__(self, self.table_name)

    def get(self, id, offset=None, limit=None):
        obj = DBModel.get(self, id)
        obj.price_data = json.dump(obj.price_data)
        return obj

    def save(self, obj):
        obj.price_data = json.loads(obj.price_data)
        return DBModel.save(self, obj)

    def update(self, symbol, price, vol):
        id = self.generate_id(symbol)
        price_data = []
        obj = self.get(id)
        if obj:
            print 'debug ', json.dump(price_data)
            price_data.append(price)
            obj.price_data = price_data
        else:
            obj = StockData(id, symbol, price, vol, price_data)
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
        return StockData(data[0], data[1], data[2], data[3], data[4])

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
