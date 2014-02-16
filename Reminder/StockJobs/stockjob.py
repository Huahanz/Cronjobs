from Reminder.WebCrawlers import webcrawler
from Reminder.EmailManager import emailmanager
from Reminder.ConditionManagers import stockconditionmanager
from Reminder.Models import stockdatamodel
from random import randint
from threading import Thread

import datetime
import sys


class StockJob:
    nasdaq_url_prefix = 'http://www.nasdaq.com/symbol/'
    nasdaq_after_hours_suffix = '/after-hours'
    nasdaq_premarket_suffix = '/premarket'
    body = ""
    url_suffix = ""
    nasdaq_pattern = "qwidget-dollar"
    wc = None
    scm = None

    def __init__(self):
        pass

    def set_env(self):
        now = self.get_now()
        weekday = now.weekday()
        if weekday == 5 or weekday == 6:
            print 'market close during weekend'
            sys.exit(0)
        premarket_start = now.replace(hour=2, minute=0, second=0, microsecond=0)
        market_open = now.replace(hour=6, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=13, minute=0, second=0, microsecond=0)
        after_hours_close = now.replace(hour=17, minute=0, second=0, microsecond=0)
        print now, ':',
        if now < premarket_start or now > after_hours_close:
            print 'market not open. exit'
            sys.exit(0)
        if now < market_open:
            print 'using premarket',
            self.url_suffix = self.nasdaq_premarket_suffix
        elif now > market_close:
            print 'using after hours',
            self.url_suffix = self.nasdaq_after_hours_suffix
        else:
            print 'normal hours',

    def is_price_valid(self, symbol, new_price):
        sdmodel = stockdatamodel.StockDataModel()
        price = self.parse_to_int(sdmodel.get_price_by_symbol(symbol))
        new_price = self.parse_to_int(new_price)
        is_valid = (new_price > price * 0.5) and (new_price < price * 2)
        #print 'checking price ', price, ' valid : ', is_valid
        return is_valid

    def escape_price(self, val):
        if isinstance(val, basestring):
            val = val.replace(",", "")
        return val

    def parse_to_int(self, val):
        return round(float(val))

    def wrap_and_send_email(self):
        if len(self.body) > 0:
            em = emailmanager.EmailManager()
            em.send_to_defaults('Stock Alert', self.body)
            num = randint(1, 100)
            if num < 33:
                em.send_email_to_single_address_gmail('6509317719@tmomail.com', 'huahanzh@gmail.com', 'testemail123',
                                                      'alert', self.body)

    def run_earning_calander(self):
        ec_url_prefix = 'http://biz.yahoo.com/research/earncal/'
        now = self.get_now()
        ec_url_date = self.date_format_pad_zero(now.year) + self.date_format_pad_zero(
            now.month) + self.date_format_pad_zero(now.day)
        url = ec_url_prefix + ec_url_date + '.html'
        # pattern = "finance.yahoo.com\/q\?s="
        print 'url' + url
        wc = webcrawler.WebCrawler()
        stock_list = self.get_watch_list()
        match_list = []
        for symbol in stock_list:
            symbol = self.get_earning_calander_reg(symbol)
            pattern = symbol
            does_match = wc.search_pattern(url, pattern)
            if does_match:
                match_list.append(pattern)

        if match_list:
            self.body += 'Earning report found : '
            self.body = self.body.join(match_list)
            self.wrap_and_send_email()

    def date_format_pad_zero(self, val):
        if val <= 0:
            print 'invalid date val ' + str(val)
            sys.exit(1)
        if val < 10:
            return '0' + str(val)
        return str(val)

    def get_earning_calander_reg(self, symbol):
        return symbol.upper()

    def check_and_run_earning_calander(self):
        now = self.get_now()
        if now.hour == 1 and now.minute <= 2:
            self.run_earning_calander()

    def get_now(self):
        time_del = datetime.timedelta(hours=8)
        return datetime.datetime.now() - time_del

    def update_stock_data(self, symbol, price, vol):
        sdmodel = stockdatamodel.StockDataModel()
        sdmodel.update(symbol, price, vol)
        return

    def get_watch_list(self):
        return ['TSLA', 'YHOO', 'MSFT', 'LNKD', 'BAC', 'ATVI', 'TWTR', 'YELP', 'ZNGA', 'STEM', 'SCTY', 'RMTI',
                'RAD', 'RENN', 'SOL', 'RSOL', 'PSX', 'OXY', 'NOK', 'NFLX', 'NBG', 'NQ', 'MCP', 'MPO', 'MCK',
                'MNKD', 'JASO', 'JCP', 'HZNP', 'HIMX', 'GOOG', 'GE', 'GME', 'FRO', 'FSLR', 'FNMA', 'FMCC', 'FB', 'DANG',
                'DRYS', 'SID', 'BBRY', 'BIDU', 'ABIO', 'AAPL', 'AMGN', 'AGNC', 'APP', 'AMZN', 'ANR', 'AMD', 'AVTC',
                'WUBA']

    def run_by_watch_list(self):
        self.set_env()
        self.wc = webcrawler.WebCrawler()
        watch_list = self.get_watch_list()
        self.scm = stockconditionmanager.StockConditionManager()
        threads = []
        for symbol in watch_list:
            thread = Thread(target=self.run, args=(symbol))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.wrap_and_send_email()

    def run(self, symbol):
        msg = self.get_now() + ":"
        url = self.nasdaq_url_prefix + symbol.lower() + self.url_suffix
        result = self.wc.search_pattern_follow_reg(url, self.nasdaq_pattern, "\$[0123456789.,]*")
        if result:
            result = self.escape_price(result)
            self.update_stock_data(symbol, result, 0)
            if self.is_price_valid(symbol, result):
                if self.scm.does_meet_nasdaq(symbol, result):
                    self.body += 'symbol : ' + symbol + ' : price : ' + result + '<br>'
                    msg += ':SEND_EMAIL:' + symbol.upper() + ':' + result
                    print msg
                    return
            msg += ':SKIP:' + symbol.upper() + ':' + result
        else:
            msg += 'wrong web ' + symbol
        print msg

sj = StockJob()
sj.run_by_watch_list()
sj.check_and_run_earning_calander()
print '======================='
