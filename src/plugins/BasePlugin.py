import abc


class BasePlugin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def process(self,host):
        pass

    @staticmethod
    @abc.abstractmethod
    def parse(content):
        pass
