from Reminder.WebCrawlers import webcrawler
from Reminder.EmailManager import emailmanager
from Reminder.ConditionManagers import conditionmanager
from Reminder.Models import nasdaqstockmodel

import datetime
import sys


class StockJob:
    nasdaq_url_prefix = 'http://www.nasdaq.com/symbol/'
    nasdaq_after_hours_suffix = '/after-hours'
    nasdaq_premarket_suffix = '/premarket'
    emailmanager = None
    conditionmanager = None
    body = ""

    def __init__(self):
        self.emailmanager = emailmanager.EmailManager()
        self.conditionmanager = conditionmanager.ConditionManager()

    def set_env(self, stock_obj):
        time_del = datetime.timedelta(hours=8)
        now = datetime.datetime.now() - time_del
        weekday = now.weekday()
        if weekday == 5 or weekday == 6:
            print 'market close during weekend'
            sys.exit(0)
        premarket_start = now.replace(hour=2, minute=0, second=0, microsecond=0)
        market_open = now.replace(hour=6, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=13, minute=0, second=0, microsecond=0)
        after_hours_close = now.replace(hour=17, minute=0, second=0, microsecond=0)
        print now, '     :        '
        if now < premarket_start or now > after_hours_close:
            print 'market not open. exit'
            sys.exit(0)
        curl_url = self.nasdaq_url_prefix + stock_obj.symbol
        if now < market_open:
            print 'using premarket'
            curl_url += self.nasdaq_premarket_suffix
        elif now > market_close:
            print 'using after hours'
            curl_url += self.nasdaq_after_hours_suffix
        else:
            print 'normal hours'
        return webcrawler.WebCrawler(curl_url, stock_obj.pattern)

    def run(self, webcrawler, stock_obj):
        if webcrawler:
            result = webcrawler.search_pattern()
            if result:
                if self.conditionmanager.is_larger_than(result, stock_obj.max) or self.conditionmanager.is_lower_than(
                        result, stock_obj.min):
                    self.body += 'symbol : ' + stock_obj.symbol + ' : price : ' + result + '<br>'
                    return True
                else:
                    print 'skip sending email for : ' + stock_obj.symbol + ' : price : ' + result
                    return False

    def wrap_and_send_email(self):
        if len(self.body) > 0:
            self.emailmanager.send_email_to_single_address_gmail('huahanzh@gmail.com', 'huahanzh@gmail.com',
                                                                 'testemail123', 'alert from nasdaq stock', self.body)
            print "sent email : " + self.body

        #       self.emailmanager.send_email_to_single_address_gmail('6509317719@tmomail.com', 'huahanzh@gmail.com', 'testemail123', 'alert', body)

    def get_list_from_db(self):
        model = nasdaqstockmodel.NasdaqStockModel()
        return model.get_all()

    def run_list_from_db(self):
        stock_list = self.get_list_from_db()

    def run_list(self):
        stock_list = self.get_list_from_db()
        for stock_obj in stock_list:
            webcrawler = self.set_env(stock_obj)
            email_sent = self.run(webcrawler, stock_obj)
        self.wrap_and_send_email()


sj = StockJob()
#sj.run_list()
sj.run_list()
