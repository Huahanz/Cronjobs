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

    ANALYSIS_PRICE_DATA = False
    json_field = 'price_data'

    def __init__(self):
        DBModel.__init__(self, True)

    def get(self, id, offset=None, limit=None):
        return DBModel.get(self, id)

    def save(self, obj):
        return DBModel.save(self, obj)

    def update(self, symbol, price, vol):
        id = self.generate_id(symbol)
        price_data = []
        obj = self.get(id)
        if obj:
            if not isinstance(obj, basestring):
                obj = obj[0]
	    if self.ANALYSIS_PRICE_DATA:
                if not obj.price_data:
                    obj.price_data = []
                obj.price_data.append(price)
            obj.vol = vol
            obj.price = price
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
        price_data = []
        if data[4]:
            price_data = json.loads(data[4])
        return StockData(data[0], data[1], data[2], data[3], price_data)

    def wrap_to_data(self, obj):
        obj.price_data = json.dumps(obj.price_data)
        return obj

    def get_price_by_symbol(self, symbol):
        id = self.generate_id(symbol)
        entry = self.get(id)
        if isinstance(entry, (list, tuple)):
            if not entry:
                return None
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
