from Reminder.DB.dydbwrapper import DYDBWrapper

class DYDBModel:
    dydbw = DYDBWrapper()

    def __init__(self):
        pass

    def get(self, key):
        return self.dydbw.select(self.table_name, key)

    def insert_by_overwrite(self, item_data):
        return self.dydbw.insert(self.table_name, item_data)

    def update(self, key, updates):
        return self.dydbw.update(self.table_name, key, updates)

    def update_or_insert(self, key, updates):
        exists = self.get(key)
        if not exists:
            updates[self.primary_key] = key
            return self.insert_by_overwrite(updates)
        else:
            return self.update(key, updates)

    def delete(self, key):
        exists = self.get(key)
        if exists:
            return self.dydbw.delete(self.table_name, key)
        return False
