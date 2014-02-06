import re

from Reminder.HttpManager import httpmanager


class WebCrawler:
    pattern = None
    web_content = None

    def __init__(self, url, pattern):
        self.web_content = self.crawle_url(url)
        self.pattern = pattern

    def crawle_url(self, url):
        http_manager = httpmanager.HttpManager()
        return http_manager.make_request_by_get(url)

    def search_pattern_follow_reg(self, reg):
        # web_content = self.crawle_url(url)
        if self.web_content and self.pattern:
            p = re.compile(self.pattern)
            for m in p.finditer(self.web_content):
                #price = self.find_price(m.start() + len(self.pattern))
                match = self.find_reg(m.start() + len(self.pattern), reg)
                if match:
                    match = match[1:]
                    return match
        return 'No match'

    def search_pattern_follow_reg_list(self, reg_list):
        rets = []
        print ''.join(reg_list)
        if self.web_content and self.pattern:
            p = re.compile(self.pattern)
            for m in p.finditer(self.web_content):
                match = self.find_reg_list(m.start() + len(self.pattern), reg_list)
                print match
                if match:
                    rets.append(match[1:])
        return rets

    def find_reg(self, start_index, reg):
        str = self.web_content[start_index:]
        p = re.compile(reg)
        for m in p.finditer(str):
            match = str[m.start():m.end()]
            if match:
                return match
        return None

    def find_reg_list(self, start_index, reg_list):
        for reg in reg_list:
            match = self.find_reg(start_index, reg)
            if match:
                return match

    def test(self, str, pattern):
        p = re.compile(pattern)
        for m in p.finditer(str):
            print str[m.start():]
            print str[m.start():m.end()]

    def find_price(self, start_index):
        while self.web_content[start_index].isdigit() == 0:
            start_index += 1
        ix = start_index + 1
        while ix < len(self.web_content):
            if self.web_content[start_index:ix].isdigit() == 0:
                break
            ix += 1
        price = self.web_content[start_index:ix - 1]
        if price.isdigit():
            return price
        return None

    def search_string(self, url, needle):
        web_content = self.crawle_url(url)
        start = 0
        while 1:
            m = web_content.find(needle, start)
            if m:
                m += len(needle)
                while web_content[m].isdigit() == 0:
                    m += 1
                ix = m + 1
                while ix < len(web_content):
                    if web_content[m:ix].isdigit() == 0:
                        break
                    ix += 1
                num = web_content[m:ix - 1]
                print url + 'price ' + num + '\n'
                start = ix
            else:
                print 'no match'
                return

#wc = WebCrawler("http://www.nasdaq.com/symbol/yhoo", "qwidget-dollar")
#print wc.search_pattern()
#wc.test("@   \">$34.96</div>", "\$[0123456789.]*")
