class ConditionManager:
    def __init__(self):
        return

    def does_meet_expr_condition(self, expr):
        return expr == 1

    def is_larger_than(self, num, base):
        try:
            num_f = float(num)
            base_f = float(base)
        except ValueError:
            return False
        return num_f > base_f

    def is_lower_than(self, num, base):
        try:
            num_f = float(num)
            base_f = float(base)
        except ValueError:
            return False
        return num_f < base_f

    def is_int_larger_than_int(self, num, base):
        num = self.parse_int(num)
        base = self.parse_int(base)
        if isinstance(num, int) and isinstance(base, int):
            return num > base
        return False

    def is_int_lower_than_int(self, num, base):
        num = self.parse_int(num)
        base = self.parse_int(base)
        if isinstance(num, int) and isinstance(base, int):
            return num < base
        return False

    def is_equal(self, num, base):
        return num == base

    def parse_int(self, num):
        if isinstance(num, int):
            return num
        elif isinstance(num, basestring):
            return int(num)
        return None

#cm = ConditionManager()
#print cm.is_larger_than("a", "1.1")
