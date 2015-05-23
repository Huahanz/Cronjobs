from Reminder.WebCrawlers import webcrawler
from Reminder.Models import wcjobmodel
from random import randint
from threading import Thread
from time import sleep
import datetime
import sys
import time
from apns import APNs, Frame, Payload


class WCCronJob:
    def __init__(self):
        self.enter_time = self.get_now()
        self.wc = webcrawler.WebCrawler()
        self.apns = APNs(use_sandbox=True, cert_file='LocalTestCert.pem', key_file='LocalTestKeyNP.pem')

        # Send a notification
        # token_hex = 'd6915bfdc113c048a04666f61b733916ec23ef6db0c0b2c1081ec9f721df8c33'
        # self.apns.gateway_server.send_notification(token_hex, payload)

        # Send multiple notifications in a single transmission
        self.frame = Frame()
        self.identifier = 1
        self.expiry = time.time() + 3600
        self.priority = 10

        pass

    def set_env(self):
        pass

    @staticmethod
    def get_now():
        time_del = datetime.timedelta(hours=8)
        return datetime.datetime.now() - time_del

    def run(self, wj):
        sleep(0.2)
        msg = unicode(self.get_now()) + ":"
        url = wj.url
        result = self.wc.search_pattern(url, wj.pattern)
        if result:
            msg += 'Found' + url + ':' + result
            device_token = 'd6915bfdc113c048a04666f61b733916ec23ef6db0c0b2c1081ec9f721df8c33'
            payload = Payload(alert="Hello World!", sound="default", badge=1)
            self.add_to_push_notification(device_token, payload)
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
        self.apns.gateway_server.send_notification_multiple(self.frame)

    def add_to_push_notification(self, device_token, payload):
        self.frame.add_item(device_token, payload, self.identifier, self.expiry,
                            self.priority)


wc = WCCronJob()
wc.run_by_list()
print '======================='
