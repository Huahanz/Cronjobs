from WebCrawlers import webcrawler
from EmailManager import emailmanager
from ConditionManagers import conditionmanager

class StockJob:
    webcrawler = None
    emailmanager = None
    conditionmanager = None
    def __init__(self):
        self.webcrawler = webcrawler.WebCrawler('http://www.nasdaq.com/symbol/tsla', 'qwidget-dollar')
        self.emailmanager = emailmanager.EmailManager()
        self.conditionmanager = conditionmanager.ConditionManager()

    def run(self):
        if self.webcrawler:
            result = self.webcrawler.search_pattern()
            if result:
                if self.conditionmanager.is_int_larger_than(result, 169):
                    self.emailmanager.send_email_to_single_address_gmail('huahanzh@gmail.com', 'huahanzh@gmail.com', 'testemail123', 'alert', result)

sj = StockJob()
sj.run()
