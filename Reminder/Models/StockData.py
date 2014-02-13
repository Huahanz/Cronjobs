class StockData:
    id = None
    symbol = None
    price = 0
    val = 0

    def __init__(self, id, symbol, price, vol):
        self.id = id
        self.symbol = symbol
        self.price = price
	self.vol = vol

