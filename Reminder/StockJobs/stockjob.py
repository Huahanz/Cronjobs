from Reminder.WebCrawlers import webcrawler
from Reminder.EmailManager import emailmanager
from Reminder.ConditionManagers import stockconditionmanager
from Reminder.Models import stockdatamodel
from Reminder.Models import nqstockdatamodel
from random import randint
from threading import Thread
from time import sleep
import datetime
import sys


class StockJob:
    nasdaq_url_prefix = 'http://www.nasdaq.com/symbol/'
    nasdaq_after_hours_suffix = '/after-hours'
    nasdaq_premarket_suffix = '/premarket'
    body = ""
    earning_report = False
    stock_alert = False
    url_suffix = ""
    nasdaq_pattern = "qwidget-dollar"
    wc = None
    scm = None
    enter_time = None
    TEST_MODE = False
    EARNING_REPORT_RANGE = 23
    TEXT_THRESHOLD = 1

    def __init__(self):
        self.enter_time = self.get_now()
        pass

    def set_env(self):
        now = self.get_now()
        weekday = now.weekday()
        if weekday == 5 or weekday == 6:
            print 'market close during weekend'
            if not self.TEST_MODE:
                sys.exit(0)
        premarket_start = now.replace(hour=2, minute=0, second=0, microsecond=0)
        market_open = now.replace(hour=6, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=13, minute=0, second=0, microsecond=0)
        after_hours_close = now.replace(hour=17, minute=0, second=0, microsecond=0)
        print now, ':',
        if now < premarket_start or now > after_hours_close:
            print 'market not open. exit'
            if not self.TEST_MODE:
                sys.exit(0)
        if now < market_open:
            print 'using premarket'
            self.url_suffix = self.nasdaq_premarket_suffix
        elif now > market_close:
            print 'using after hours'
            self.url_suffix = self.nasdaq_after_hours_suffix
        else:
            print 'normal hours'

    def is_price_valid(self, symbol, new_price):
        sdmodel = stockdatamodel.StockDataModel()
        price = self.parse_to_int(sdmodel.get_price_by_symbol(symbol))
        new_price = self.parse_to_int(new_price)
        is_valid = (new_price > price * 0.5) and (new_price < price * 2)
        if not is_valid:
            print 'checking price ', price, ' valid : ', is_valid, ' ____ ', new_price
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
            title = "Stock Msg"
            if self.earning_report and self.stock_alert:
                title = "Earning Report AND Stock Alert"
            elif self.earning_report:
                title = "Earning Report"
            elif self.stock_alert:
                title = "Stock Alert"

            em.send_to_defaults(title, self.body)
            num = randint(1, 100)
            if num < self.TEXT_THRESHOLD:
                em.send_text_by_defaults(title, self.body)

    def __run_earning_calander(self, start_date):
        ec_url_prefix = 'http://biz.yahoo.com/research/earncal/'
        ec_url_date = self.date_format_pad_zero(start_date.year) + self.date_format_pad_zero(
            start_date.month) + self.date_format_pad_zero(start_date.day)
        url = ec_url_prefix + ec_url_date + '.html'
        # pattern = "finance.yahoo.com\/q\?s="
        print 'url ' + url
        wc = webcrawler.WebCrawler()
        stock_list = self.get_watch_list()
        match_dict = {}
        for symbol in stock_list:
            symbol = self.get_earning_calander_reg(symbol)
            pattern = "[\b\>]" + symbol + "[\b\<]"
            #does_match = wc.search_pattern(url, pattern)
            other_info_pattern = "\<small\>[\s\w\:]*\<"
            does_match = wc.search_pattern_follow_reg(url, pattern, other_info_pattern)
            if does_match:
                match_dict[symbol] = does_match

        if match_dict:
            for k, v in match_dict.items():
                self.body += ec_url_date + ' : ' + str(start_date.weekday() + 1) + ' :  Earning report found : '
                self.body += k + " : " + v[6:-1]
                self.body += """ \r\n"""
            self.earning_report = True

    def run_earning_calander(self, start_date):
        ec_url_prefix = 'http://biz.yahoo.com/research/earncal/'
        ec_url_date = self.date_format_pad_zero(start_date.year) + self.date_format_pad_zero(
            start_date.month) + self.date_format_pad_zero(start_date.day)
        url = ec_url_prefix + ec_url_date + '.html'
        pattern = "finance.yahoo.com\/q\?s="
        print 'url' + url
        wc = webcrawler.WebCrawler()
        stock_list = self.get_watch_list()
        match_list = []
        for symbol in stock_list:
            symbol = self.get_earning_calander_reg(symbol)
            match_list.append(symbol)
        matches = wc.search_pattern_follow_exact_match_list(url, pattern, match_list)
        print 'matchs', matches
        if matches:
            print 'body', self.body
            self.body += 'Earning report found : '
            self.body = self.body.join(matches)

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
        if self.TEST_MODE or now.minute == 1:
            start_date = self.get_now()
            for i in range(0, self.EARNING_REPORT_RANGE):
                self.__run_earning_calander(start_date)
                start_date += datetime.timedelta(1)

    def get_now(self):
        time_del = datetime.timedelta(hours=8)
        return datetime.datetime.now() - time_del

    def update_stock_data(self, symbol, price, vol):
        sdmodel = stockdatamodel.StockDataModel()
        sdmodel.update(symbol, price, vol)
        nqmodel = nqstockdatamodel.NQStockDataModel()
        prefix = self.enter_time.strftime("%H:%M:%S")
        key = symbol + "-" + self.enter_time.strftime("%y-%m-%d")
        #nqmodel.update_price(key, {prefix: price})
        return

    def get_watch_list(self):
        return ['TSLA', 'YHOO', 'MSFT', 'LNKD', 'BAC', 'ATVI', 'TWTR', 'YELP', 'ZNGA', 'STEM', 'SCTY', 'RMTI',
                'RAD', 'RENN', 'SOL', 'RSOL', 'PSX', 'OXY', 'GOGO', 'LIVE', 'PLUG', 'WB', 'YOKU', 'NMBL', 'VJET', 'JNUG', 'SPY', 'NOK', 'NFLX', 'NBG', 'NQ', 'MCP', 'MPO', 'MCK',
                'MNKD', 'JASO', 'JCP', 'HZNP', 'HIMX', 'GOOG', 'GE', 'GME', 'FRO', 'FSLR', 'FNMA', 'FMCC', 'FB', 'DANG',
                'DRYS', 'SID', 'BBRY', 'BIDU', 'ABIO', 'AAPL', 'AMGN', 'AGNC', 'APP', 'AMZN', 'ANR', 'AMD', 'AVTC',
                'WUBA', 'VNET', 'JOBS', 'CYOU', 'CNTF', 'EFUT', 'KONE', 'NINE', 'PACT', 'SINA', 'SOHU', 'GOMO', 'YY', 'KING', 'CMGE', 'PWRD', 'QIHU', 'QUNR','XNET', 'KNDI','BABA','JD']

    def run_by_watch_list(self):
        self.set_env()
        self.wc = webcrawler.WebCrawler()
        watch_list = self.get_watch_list()
        self.scm = stockconditionmanager.StockConditionManager()
        threads = []
        for symbol in watch_list:
            thread = Thread(target=self.run, args=(symbol, ))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def run(self, symbol):
        sleep(0.2)
        msg = unicode(self.get_now()) + ":"
        url = self.nasdaq_url_prefix + symbol.lower() + self.url_suffix
        result = self.wc.search_pattern_follow_reg(url, self.nasdaq_pattern, "\$[0123456789.,]*")
        if result:
            result = self.escape_price(result)
            self.update_stock_data(symbol, result, 0)
            if self.is_price_valid(symbol, result):
                if self.scm.does_meet_nasdaq(symbol, result):
                    self.stock_alert = True
                    self.body += 'symbol : ' + symbol + ' : price : ' + result + '<br>'
                    msg += ':SEND_EMAIL:' + symbol.upper() + ':' + result
                    print msg
                    return
            msg += ':SKIP:' + symbol.upper() + ':' + result
        else:
            msg += 'wrong web ' + symbol
        print msg


sj = StockJob()
if len(sys.argv) >= 2:
    sj.TEST_MODE = True
    sj.EARNING_REPORT_RANGE = 14
if len(sys.argv) >= 3:
    sj.EARNING_REPORT_RANGE = 31
sj.run_by_watch_list()
sj.check_and_run_earning_calander()
sj.wrap_and_send_email()
print '======================='
