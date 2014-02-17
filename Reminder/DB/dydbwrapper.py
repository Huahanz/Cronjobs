import boto
import boto.dynamodb
import decimal
import atexit


class DYDBWrapper:
    region = None
    conn = None
    write_queue = {}
    unit = 10

    def __init__(self, region='us-east-1'):
        self.region = region
        atexit.register(self.flush_batch_writes)

    def connet(self):
        if not self.conn:
            self.conn = boto.dynamodb.connect_to_region(self.region)

    def select(self, table_name, key):
        if not key or not table_name:
            return None
        self.connet()
        table = self.conn.get_table(table_name)
        if not table:
            return None
        try:
            item = table.get_item(hash_key=key)
        except:
            return None
        return item

    def delete(self, table_name, key):
        if not key or not table_name:
            return False
        self.connet()
        table = self.conn.get_table(table_name)
        if not table:
            return False
        item = table.get_item(hash_key=key)
        item.delete()
        return True

    def update(self, table_name, key, updates):
        item = self.select(table_name, key)
        if not item:
            return "INEXIST"
        for k, v in updates.iteritems():
            item[k] = v
        self.enqueue_batch_writes(table_name, key, item)
        return True

    def insert(self, table_name, key, item_data):
        if not item_data or not table_name:
            return False
        self.connet()
        table = self.conn.get_table(table_name)
        if not table:
            return False
        item = table.new_item(attrs=item_data)
        self.enqueue_batch_writes(table_name, key, item)
        return True

    def enqueue_batch_writes(self, table_name, key, item):
        print 'enqueue ', table_name, ', ', item
        if table_name not in self.write_queue:
            self.write_queue[table_name] = {}
        if key not in self.write_queue[table_name]:
            self.write_queue[table_name][key] = []
        self.write_queue[table_name][key].append(item)

    def flush_batch_writes(self):
        print 'flushing '
        self.connet()
        batch_item_list = self.__group_batch_items()
        self.__send_batch(batch_item_list)

    def __group_batch_items(self):
        batch_item_list = {}
        for table_name, item_dict in self.write_queue.iteritems():
            table = self.conn.get_table(table_name)
            item_list = []
            for key, items in item_dict.iteritems():
                merged_item = table.new_item(attrs={})
                for item in items:
                    merged_item = dict(merged_item.items() + item.items())
                item_list.append(merged_item)
            batch_item_list[table_name] = item_list
        return batch_item_list

    def __send_batch(self, batch_item_list):
        batch_list = self.conn.new_batch_write_list()
        buffer_list = []
        for table_name, item_list in batch_item_list.iteritems():
            table = self.conn.get_table(table_name)
            for item in item_list:
                buffer_list.append(item)
                if len(buffer_list) > self.unit:
                    batch_list.add_batch(table, buffer_list)
                    self.conn.batch_write_item(batch_list)
                    batch_list = self.conn.new_batch_write_list()
                    buffer_list = []
            if buffer_list:
                batch_list.add_batch(table, buffer_list)
                self.conn.batch_write_item(batch_list)
                buffer_list = []
                batch_list = self.conn.new_batch_write_list()

# dy = DYDBWrapper()
# tb_name = 'nq_stock_price_data'
# dy.insert(tb_name, 'LNKD99', {'symbol': 'LNKD99', 'price': 1129.1})
# print '1 : ', dy.select(tb_name, 'LNKD99')
# dy.insert('test', 'LNKD99', {'id': 'LNKD99', 'price': 14.1})
# dy.insert('test', 'LNKD99', {'id': 'LNKD99', 'price1': 1.1})
# dy.insert('test', 'LNKD99', {'id': 'LNKD99', 'pri': 12.1})
# print '2 : ', dy.select(tb_name, 'LNKD99')
