import abc

class BaseObject:
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        pass
    @abc.abstractmethod
    def generate_id(self):
        pass