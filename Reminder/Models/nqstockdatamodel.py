from dydbmodel import DYDBModel
import datetime


class NQStockDataModel(DYDBModel):
    table_name = 'nq_stock_data'

    def __init__(self):
        DYDBModel.__init__(self)

    def get(self, symbol):
        key = self.generate_key(symbol)
        return DYDBModel.get(self, key)

    def update_price(self, symbol, price_data):
        key = self.generate_key(symbol)
        price_data['symbol'] = key
        return DYDBModel.save(self, price_data)

    def generate_key(self, symbol):
        date = datetime.datetime.today()
        return symbol.upper() + date

        # nm = NQStockDataModel()
        # print nm.get('tsla')
        # nm.update_price('tsla', 202)
        # print nm.get('tsla')