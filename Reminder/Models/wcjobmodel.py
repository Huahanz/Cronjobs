from Reminder.Models.WCJob import WCJob
from Reminder.Models.dbmodel import DBModel


class WCJobModel(DBModel):
    table_name = 'wctask'
    schema = [
        ['id', 'int'],
        ['url', 'string'],
        ['pattern', 'string'],
        ['patternCount', 'int'],
        ['wctype', 'int'],
        ['uuid', 'string']
    ]

    def __init__(self):
        DBModel.__init__(self, True)

    def get(self, id, offset=None, limit=None):
        return DBModel.get(self, id)

    def wrap_to_obj(self, data):
        if len(data) != len(self.schema):
            print 'invalid data format'
            return None
        return WCJob(data[0], data[1], data[2], data[3], data[4])
