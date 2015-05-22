from Reminder.WebCrawlers import webcrawler
from Reminder.Models import wcjobmodel
from random import randint
from threading import Thread
from time import sleep
import datetime
import sys

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
        self.enter_time = self.get_now()
        self.wc = webcrawler.WebCrawler()
        pass

    def set_env(self):
        pass

    def get_now(self):
        time_del = datetime.timedelta(hours=8)
        return datetime.datetime.now() - time_del

    def run(self, wj):
        sleep(0.2)
        msg = unicode(self.get_now()) + ":"
        url = wj.url
        result = self.wc.search_pattern(url, wj.pattern)
        if result:
            msg += 'Found' + url + ':' + result
        else:
            msg += 'NOT Found'
        print msg

    def run_by_list(self):
        self.set_env()
        threads = []
        wcmodel = wcjobmodel.WCJobModel()
        all_l = wcmodel.get_all()
        print all_l
        for wj in all_l:
            thread = Thread(target=self.run, args=(wj, ))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

wc = WCCronJob()
wc.run_by_list()
print '======================='
