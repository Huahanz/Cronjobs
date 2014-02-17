from Reminder.DB.dydbwrapper import DYDBWrapper

class DYDBModel:
    dydbw = DYDBWrapper()

    def __init__(self):
        pass

    def get(self, key):
        return self.dydbw.select(self.table_name, key)

    def save(self, item_data):
        return self.dydbw.insert(self.table_name, item_data)

    def update(self, key, updates):
        return self.dydbw.update(self.table_name, key, updates)

    def delete(self, key):
        exists = self.get(key)
        if exists:
            return self.dydbw.delete(self.table_name, key)
        return False
