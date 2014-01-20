import os
import sys

file_path = os.path.abspath(__file__)
print(file_path)
dir_path = os.path.dirname(file_path)
print(dir_path)
base_path = os.path.dirname(dir_path)
print(base_path)
sys.path.append(base_path)
sys.path.append(base_path + '/WebCrawlers')
print(sys.path)

from Reminder.WebCrawlers import webcrawler
from Reminder.EmailManager import emailmanager
from Reminder.ConditionManagers import conditionmanager

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
