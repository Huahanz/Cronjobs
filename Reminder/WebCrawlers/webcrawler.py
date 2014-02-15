import re

from Reminder.HttpManager import httpmanager


class WebCrawler:

    def __init__(self):
        pass

    def craw_url(self, url):
        http_manager = httpmanager.HttpManager()
        return http_manager.make_request_by_get(url)

    def search_pattern(self, url, pattern):
        web_content = self.craw_url(url)
        if web_content and pattern:
            p = re.compile(pattern)
            for m in p.finditer(str):
                match = str[m.start():m.end()]
                if match:
                    return match
        return None

    def search_pattern_follow_reg(self, url, pattern, reg):
        web_content = self.craw_url(url)
        if web_content and pattern:
            p = re.compile(pattern)
            for m in p.finditer(web_content):
                #price = self.__find_price(web_content, m.start() + len(pattern))
                match = self.__find_reg(web_content, m.start() + len(pattern), reg)
                if match:
                    match = match[1:]
                    return match
        return 'No match'

    def search_pattern_follow_reg_list(self, url, pattern, reg_list):
        web_content = self.craw_url(url)
        rets = []
        if web_content and pattern:
            p = re.compile(pattern)
            for m in p.finditer(web_content):
                match = self.__find_reg_list(web_content, m.start() + len(pattern), reg_list)
                if match:
                    rets.append(match[1:])
        return rets

    def __find_reg(self, web_content, start_index, reg):
        str = web_content[start_index:]
        #print 'rr ', reg, str[:100]
        p = re.compile(reg)
        for m in p.finditer(str):
            match = str[m.start():m.end()]
            if match:
                return match
        return None

    def __find_reg_list(self, web_content, start_index, reg_list):
        for reg in reg_list:
            match = self.__find_reg(web_content, start_index, reg)
            if match:
                return match

    def test(self, str, pattern):
        p = re.compile(pattern)
        for m in p.finditer(str):
            print str[m.start():]
            print str[m.start():m.end()]

    def __find_price(self, web_content, start_index):
        while web_content[start_index].isdigit() == 0:
            start_index += 1
        ix = start_index + 1
        while ix < len(web_content):
            if web_content[start_index:ix].isdigit() == 0:
                break
            ix += 1
        price = web_content[start_index:ix - 1]
        if price.isdigit():
            return price
        return None

    def search_string(self, url, needle):
        web_content = self.craw_url(url)
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
