import conditionmanager
from Reminder.Models import nasdaqstockmodel


class StockConditionManager(conditionmanager.ConditionManager):
    def __init__(self):
        conditionmanager.ConditionManager.__init__(self)

    def does_meet_nasdaq(self, symbol, price):
        nm = nasdaqstockmodel.NasdaqStockModel()
        stock_obj = nm.get_by_symbol(symbol)
        if not stock_obj:
            upper_symbol = symbol.upper()
            stock_obj = nm.get_by_symbol(upper_symbol)
            if stock_obj:
                nm.reformat(stock_obj)
        if stock_obj:
            return self.does_basic_match(price, stock_obj.min, stock_obj.max)
        return False

    def does_basic_match(self, price, min, max):
        return conditionmanager.ConditionManager.is_larger_than(price,
                                                                max) or conditionmanager.ConditionManager.is_lower_than(
            price, min)
