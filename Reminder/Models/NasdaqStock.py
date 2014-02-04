class NasdaqStock:
    id = None
    symbol = None
    pattern = None
    min = 0
    max = 10000

    def __init__(self, id, symbol, pattern, min, max):
	self.id = id
        self.symbol = symbol
        self.pattern = pattern
        self.min = min
        self.max = max
