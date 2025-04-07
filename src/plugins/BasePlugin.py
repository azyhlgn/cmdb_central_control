import abc


class BasePlugin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def process(self, host, executor, response):
        pass

    @staticmethod
    @abc.abstractmethod
    def parse(content):
        pass
