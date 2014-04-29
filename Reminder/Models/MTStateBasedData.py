import BaseObject


class MTStateBasedData(BaseObject.BaseObject):
    id = None
    state = 0
    state_extension = ''
    start_pattern = ''
    end_pattern = ''
    extract_start_pattern = ''
    extract_info = ''

    def __init__(self, id, state, state_extension, start_pattern, end_pattern, extract_start_pattern, extract_info):
        self.id = id
        self.state = state
        self.state_extension = state_extension
        self.start_pattern = start_pattern
        self.end_pattern = end_pattern
        self.extract_start_pattern = extract_start_pattern
        self.extract_info = extract_info
        BaseObject.BaseObject.__init__(self)

    def generate_id(self):
        pass