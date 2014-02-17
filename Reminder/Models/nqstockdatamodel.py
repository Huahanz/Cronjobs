from dydbmodel import DYDBModel


class NQStockDataModel(DYDBModel):
    table_name = 'nq_stock_data'

    def __init__(self):
        DYDBModel.__init__(self)

    def get(self, symbol):
        key = self.generate_key(symbol)
        return DYDBModel.get(self, key)

    def update_price(self, symbol, price):
        key = self.generate_key(symbol)
        return DYDBModel.save(self, {'symbol': key, 'price': price})

    def generate_key(self, symbol):
        return symbol.upper()

# nm = NQStockDataModel()
# print nm.get('tsla')
# nm.update_price('tsla', 202)
# print nm.get('tsla')