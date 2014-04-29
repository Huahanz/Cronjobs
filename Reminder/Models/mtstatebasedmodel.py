from Reminder.Models.dbmodel import DBModel
from Reminder.Models.MTStateBasedData import MTStateBasedData
import json

class MTStateBasedModel(DBModel):
    table_name = 'mt_state_based'
    schema = [
        ['url', 'string'],
        ['state', 'long'],
        ['state_extension', 'string'],
        ['start_pattern', 'string'],
        ['end_pattern', 'string'],
        ['extract_start_pattern', 'string'],
        ['extract_info', 'string']
    ]

    def __init__(self):
        DBModel.__init__(self, True)

    def get(self, id, offset=None, limit=None):
        return DBModel.get(self, id)

    def wrap_to_obj(self, data):
        if len(data) != len(self.schema):
            print 'invalid data format'
            return None
        return MTStateBasedData(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    def wrap_to_data(self, obj):
        return obj

sd = MTStateBasedModel()
ox = sd.get('www.test.com')
print ''.join(sd.get(ox))