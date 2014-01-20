from HttpManager import httpmanager
import re


class WebCrawler:
    pattern = None
    web_content = None

    def __init__(self, url, pattern):
        self.web_content = self.crawle_url(url)
        self.pattern = pattern

    def crawle_url(self, url):
        http_manager = httpmanager.HttpManager()
        return http_manager.make_request_by_get(url)

    def search_pattern(self):
        # web_content = self.crawle_url(url)
        # print web_content + '\n'
        if self.web_content and self.pattern:
            p = re.compile(self.pattern)
            for m in p.finditer(self.web_content):
                price = self.find_price(m.start() + len(self.pattern))
                if price:
                    print price
                    return price
        return 'No match'

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
                print m
                m += len(needle)
                while web_content[m].isdigit() == 0:
                    m += 1
                ix = m + 1
                while ix < len(web_content):
                    if web_content[m:ix].isdigit() == 0:
                        break
                    ix += 1
                num = web_content[m:ix - 1]
                print 'price ' + num + '\n'
                start = ix
            else:
                print 'no match'
                return
