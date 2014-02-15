import BaseObject
import json

class StockData(BaseObject.BaseObject):
    id = None
    symbol = None
    price = 0
    val = 0
    price_data = ''

    def __init__(self, id, symbol, price, vol, price_data):
        self.id = id
        self.symbol = symbol
        self.price = price
        self.vol = vol
        self.price_data = price_data
        BaseObject.BaseObject.__init__(self)

    def generate_id(self):
        id = 0
        for c in self.symbol:
            id += (ord(c) - 97)
            id *= 26
        return id