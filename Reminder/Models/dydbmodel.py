from Reminder.DB.dydbwrapper import DYDBWrapper

class DYDBModel:
    dydbw = DYDBWrapper()

    def __init__(self):
        pass

    def get(self, key):
        return self.dydbw.select(self.table_name, key)

    def insert_by_overwrite(self, key, item_data):
        return self.dydbw.insert(self.table_name, key, item_data)

    def update(self, key, updates):
        return self.dydbw.update(self.table_name, key, updates)

    def update_or_insert(self, key, updates):
        ret = self.update(key, updates)
        if ret == 'INEXIST':
            updates[self.primary_key] = key
            return self.insert_by_overwrite(key, updates)
        return True

    def delete(self, key):
        exists = self.get(key)
        if exists:
            return self.dydbw.delete(self.table_name, key)
        return False
