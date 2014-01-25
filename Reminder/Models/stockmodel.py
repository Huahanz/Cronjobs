class StockModel:

    symbol = None
    pattern = None
    min = 0
    max = 10000

    def __init__(self, symbol, pattern, min, max):
	self.symbol = symbol
	self.pattern = pattern
	self.min = min
	self.max = max

    
