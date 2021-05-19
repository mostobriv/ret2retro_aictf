import abc

class BaseStorage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_resource(self, name):
        """ Попытаться взять ресурс, если не получилось отдаем None"""

    @abc.abstractmethod
    def add_resource(self, name: str, data: bytearray):
        """ Сохранить ресурс """
        pass
