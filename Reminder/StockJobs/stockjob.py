from Reminder.WebCrawlers import webcrawler
from Reminder.EmailManager import emailmanager
from Reminder.ConditionManagers import conditionmanager

import datetime
import sys

class StockJob:
    webcrawler = None
    daytime_url = 'http://www.nasdaq.com/symbol/tsla'
    after_hours_url = 'http://www.nasdaq.com/symbol/tsla/after-hours'
    premarket_url = 'http://www.nasdaq.com/symbol/tsla/premarket'
    emailmanager = None
    conditionmanager = None
    def __init__(self):
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
	curl_url = self.daytime_url
	if now < market_open:
	    print 'using premarket'
	    curl_url = self.premarket_url
	elif now > market_close:
	    print 'using after hours'
	else:
	    print 'normal hours'
        curl_url = self.after_hours_url
	self.webcrawler = webcrawler.WebCrawler(curl_url, 'qwidget-dollar')
        self.emailmanager = emailmanager.EmailManager()
        self.conditionmanager = conditionmanager.ConditionManager()

    def run(self):
        if self.webcrawler:
            result = self.webcrawler.search_pattern()
            if result:
                if self.conditionmanager.is_int_larger_than(result, 180):
                    self.emailmanager.send_email_to_single_address_gmail('huahanzh@gmail.com', 'huahanzh@gmail.com', 'testemail123', 'alert', result)

sj = StockJob()
sj.run()
