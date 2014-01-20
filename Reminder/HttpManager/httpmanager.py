import requests


class HttpManager:

    def make_request_by_get(self, url):
        r = requests.get(url)
        return r.text

    def __init__(self):
        return
