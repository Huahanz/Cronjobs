import boto
import boto.dynamodb
import decimal


class DYDBWrapper:
    region = None
    conn = None

    def __init__(self, region='us-east-1'):
        self.region = region

    def connet(self):
        if not self.conn:
	    print 'make dy conn '
            self.conn = boto.dynamodb.connect_to_region(self.region)

    def insert(self, table_name, item_data):
        if not item_data or not table_name:
            return False
        self.connet()
        table = self.conn.get_table(table_name)
        if not table:
            return False
	print 'insert ', item_data
        item = table.new_item(attrs=item_data)
        item.put()
        return True

    def select(self, table_name, key):
        if not key or not table_name:
            return None
        self.connet()
        table = self.conn.get_table(table_name)
        if not table:
            return None
        item = table.get_item(hash_key=key)
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
        if not key or not table_name or not updates:
            return False
        self.connet()
        table = self.conn.get_table(table_name)
        if not table:
            return False
        item = table.get_item(hash_key=key)
        for k, v in updates.iteritems():
            item[k] = v
        item.put()
        return True

# dy = DYDBWrapper()
# tb_name = 'nq_stock_data'
# dy.insert(tb_name, {'symbol': 'LNKD', 'price': 189.1})
# print '1 : ', dy.select(tb_name, 'KKK')
# dy.insert(tb_name, {'symbol': 'LNKD', 'price': 179.1})
# print '1 : ', dy.select(tb_name, 'LNKD')
# dy.update(tb_name, 'LNKD', {'price': 188.2, 'new_key': 190})
# print '2 : ', dy.select(tb_name, 'LNKD')
