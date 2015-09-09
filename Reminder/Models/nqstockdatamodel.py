from dydbmodel import DYDBModel
import datetime


class NQStockDataModel(DYDBModel):
    table_name = 'nq_stock_price_data'
    primary_key = 'symbol'

    def __init__(self):
        DYDBModel.__init__(self)

    def get(self, key):
        return DYDBModel.get(self, key)

    def update_price(self, key, price_data):
        return DYDBModel.update_or_insert(self, key, price_data)

        # print nm.get('tsla')
        # nm.update_price('tsla', 202)
        # print nm.get('tsla')