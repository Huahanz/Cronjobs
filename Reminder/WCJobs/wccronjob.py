from Reminder.WebCrawlers import webcrawler
from Reminder.Models import wcjobmodel


class WCCronJob:
    # nasdaq_url_prefix = 'http://www.nasdaq.com/symbol/'
    # nasdaq_after_hours_suffix = '/after-hours'
    # nasdaq_premarket_suffix = '/premarket'
    # body = ""
    # earning_report = False
    # stock_alert = False
    # url_suffix = ""
    # nasdaq_pattern = "qwidget-dollar"
    # wc = None
    # scm = None
    # enter_time = None
    # TEST_MODE = False
    # EARNING_REPORT_RANGE = 23
    # TEXT_THRESHOLD = 1
    #
    def __init__(self):
        pass

    def set_env(self):
        pass

    # def run(self, symbol):
    #     sleep(0.2)
    #     msg = unicode(self.get_now()) + ":"
    #     url = self.nasdaq_url_prefix + symbol.lower() + self.url_suffix
    #     result = self.wc.search_pattern_follow_reg(url, self.nasdaq_pattern, "\$[0123456789.,]*")
    #     if result:
    #         result = self.escape_price(result)
    #         self.update_stock_data(symbol, result, 0)
    #         if self.is_price_valid(symbol, result):
    #             if self.scm.does_meet_nasdaq(symbol, result):
    #                 self.stock_alert = True
    #                 self.body += 'symbol : ' + symbol + ' : price : ' + result + '<br>'
    #                 msg += ':SEND_EMAIL:' + symbol.upper() + ':' + result
    #                 print msg
    #                 return
    #         msg += ':SKIP:' + symbol.upper() + ':' + result
    #     else:
    #         msg += 'wrong web ' + symbol
    #     print msg

    def run_by_list(self):
        self.set_env()
        self.wc = webcrawler.WebCrawler()
        threads = []
        wcmodel = wcjobmodel.WCJobModel()
        all_l = wcmodel.get_all()
        # for symbol in all_l:
        #     thread = Thread(target=self.run, args=(symbol, ))
        #     thread.start()
        #     threads.append(thread)
        #
        # for thread in threads:
        #     thread.join()
        print all_l

wc = WCCronJob()
wc.run_by_list()
print '======================='
