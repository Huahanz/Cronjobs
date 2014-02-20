import conditionmanager
from Reminder.Models import nasdaqstockmodel


class StockConditionManager(conditionmanager.ConditionManager):
    def __init__(self):
        conditionmanager.ConditionManager.__init__(self)

    def does_meet_nasdaq(self, symbol, price):
        nm = nasdaqstockmodel.NasdaqStockModel()
        stock_obj = nm.get_by_symbol(symbol)
        if not stock_obj:
            lower_symbol = symbol.lower()
            stock_obj = nm.get_by_symbol(lower_symbol)
            if stock_obj:
                nm.reformat(stock_obj)
        if stock_obj:
	    if not isinstance(stock_obj, basestring):
		stock_obj = stock_obj[0]
            return self.does_basic_match(price, stock_obj.min, stock_obj.max)
        return False

    def does_basic_match(self, price, min, max):
        return conditionmanager.ConditionManager.is_larger_than(self,price,
                                                                max) or conditionmanager.ConditionManager.is_lower_than(
            self, price, min)
