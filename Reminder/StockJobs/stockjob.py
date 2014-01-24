from Reminder.WebCrawlers import webcrawler
from Reminder.EmailManager import emailmanager
from Reminder.ConditionManagers import conditionmanager
from Reminder.Models import stockmodel

import datetime
import sys

class StockJob:
    nasdaq_url_prefix = 'http://www.nasdaq.com/symbol/'
    nasdaq_after_hours_suffix = '/after-hours'
    nasdaq_permarket_suffix = '/premarket'
    emailmanager = None
    conditionmanager = None
    def __init__(self):
	self.emailmanager = emailmanager.EmailManager()
        self.conditionmanager = conditionmanager.ConditionManager()

    def set_env(self, stock_obj):
        time_del = datetime.timedelta(hours=8)
	now = datetime.datetime.now() - time_del
	premarket_start = now.replace(hour=2, minute=0, second=0, microsecond=0)
	market_open = now.replace(hour=6, minute=0, second=0, microsecond=0)
	market_close = now.replace(hour=13, minute=0, second=0, microsecond=0)
	after_hours_close = now.replace(hour=17, minute=0, second=0, microsecond=0)
	print now, '     :        '	
	if now < premarket_start or now > after_hours_close:
	    print 'market not open. exit'
	    sys.exit(0)
	curl_url = self.nasdaq_url_perfix + stock_obj.symbol 
	if now < market_open:
	    print 'using premarket'
	    curl_url += self.nasdaq_permarket_suffix
	elif now > market_close:
	    print 'using after hours'
	    curl_url += self.nasdaq_after_hours_suffix
	else:
	    print 'normal hours'
        webcrawler = webcrawler.WebCrawler(curl_url, stock_obj.pattern)	
        return webcrawler

    def run(self, webcrawler, stock_obj):
        if webcrawler:
            result = webcrawler.search_pattern()
            if result:
                if self.conditionmanager.is_int_larger_than(result, stock_obj.max) or self.conditionmanager.is_int_lower_than(result, stock_obj.min):
                    self.emailmanager.send_email_to_single_address_gmail('huahanzh@gmail.com', 'huahanzh@gmail.com', 'testemail123', 'alert', result)

    def run_list(self):
	tsla = stockmodel.StockModel('tsla', 'qwidget-dollar', 130, 190)
        yahoo = stockmodel.StockModel('yhoo', 'qwidget-dollar', 35, 45) 
        bac = models.StockModel('bac', 'qwidget-dollar', 14, 18)
	stock_list = [tsla, yahoo, bac] 
	for stock_obj in stock_list:
	    webcrawler = self.set_env(stock_obj)
	    self.run(webcrawler, stock_obj)
	    	

sj = StockJob()
sj.run_list()
