import boto
import boto.dynamodb
import decimal
import atexit


class DYDBWrapper:
    region = None
    conn = None
    write_queue = {}

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
        # print 'flushing '
        self.connet()
        batch_list = self.conn.new_batch_write_list()
        for table_name, item_dict in self.write_queue.iteritems():
            table = self.conn.get_table(table_name)
            if not table:
                continue
            item_list = self.__group_batch_items(table, item_dict)
            batch_list.add_batch(table, puts=item_list)
        # print 'blist ', batch_list
        self.conn.batch_write_item(batch_list)

    def __group_batch_items(self, table, item_dict):
        item_list = []
        for key, items in item_dict.iteritems():
            merged_item = table.new_item(attrs={})
            for item in items:
                merged_item = dict(merged_item.items() + item.items())
            item_list.append(merged_item)
        return item_list

dy = DYDBWrapper()
tb_name = 'nq_stock_price_data'
dy.insert(tb_name, 'LNKD100', {'symbol': 'LNKD100', 'price': 1129.1})
print '1 : ', dy.select(tb_name, 'LNKD100')
dy.insert('test', 'LNKD100', {'id': 'LNKD100', 'price': 14.1})
dy.insert('test', 'LNKD100', {'id': 'LNKD100', 'price1': 1.1})
dy.insert('test', 'LNKD100', {'id': 'LNKD100', 'pri': 12.1})
# dy.insert(tb_name, {'symbol': 'LNKD100', 'price': 209.1})
# dy.insert(tb_name, {'symbol': 'LNKD100', 'price1': 209.1})
# dy.insert(tb_name, {'symbol': 'LNKD100', 'price2': 209.1})
# print '1 : ', dy.select(tb_name, 'LNKD100')
# dy.update(tb_name, 'LNKD100', {'price': 188.2, 'new_key': 190})
# print '1 : ', dy.select(tb_name, 'LNKD100')
print '2 : ', dy.select(tb_name, 'LNKD100')
