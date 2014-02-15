import BaseObject

class StockData(BaseObject):
    id = None
    symbol = None
    price = 0
    val = 0

    def __init__(self, id, symbol, price, vol):
        self.id = id
        self.symbol = symbol
        self.price = price
        self.vol = vol
        BaseObject.BaseObject.__init__()

    def generate_id(self):
        id = 0
        for c in self.symbol:
            id += (ord(c) - 97)
            id *= 26
        return id