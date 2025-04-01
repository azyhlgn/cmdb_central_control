import logging

from lib.conf.config import settings


class LogFactory(object):

    def __init__(self, filename, level, logger_name):
        file_handler = logging.FileHandler(filename, 'a', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(settings.LOGGER_FORMAT))
        self._logger = logging.Logger(logger_name, level=level)
        self._logger.addHandler(file_handler)

    def error(self, msg):
        self._logger.error(msg)


# 通过导入方式实现的单例模式
run_logger = LogFactory(settings.RUN_LOG_FILE, logging.DEBUG, 'run_logger')
error_logger = LogFactory(settings.ERROR_LOG_FILE, logging.ERROR, 'error_logger')