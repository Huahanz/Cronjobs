import urllib, urllib2, cookielib
import encodings, os

class MtJob:
    def __init__(self):
        pass

    def fetch(self, url):
        pass

    def run(self):
        pass


# do POST
url_2 = 'http://www.mitbbs.com/mitbbs_bbsbfind.php?board=JobHunting'
values = dict(board='JobHunting', title='', title2='', title3='', userid='nipoleon', dt='333', year='', month='', day='', opflag=0, submit='%B5%DD%BD%BB%B2%E9%D1%AF%BD%E1%B9%FB')
#board=JobHunting&title=&title2=&title3=&userid=nipoleon&dt=7&year=&month=&day=&opflag=0&submit=%B5%DD%BD%BB%B2%E9%D1%AF%BD%E1%B9%FB
data = urllib.urlencode(values)
req = urllib2.Request(url_2, data)
rsp = urllib2.urlopen(req)
content = rsp.read()

print content.decode('utf16')