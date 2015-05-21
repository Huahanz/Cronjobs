import BaseObject


class WCJob(BaseObject.BaseObject):
    id = 0
    url = None
    pattern = None
    patternCount = 0
    wctype = 0
    uuid = None

    def __init__(self, id, url, pattern, patternCount, wctype, uuid):
        self.id = id
        self.symbol = url
        self.pattern = pattern
        self.patternCount = patternCount
        self.wctype = wctype
        self.uuid = uuid
        BaseObject.BaseObject.__init__(self)

    def generate_id(self):
        return id
