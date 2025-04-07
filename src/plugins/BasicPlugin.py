import traceback

from src.plugins import BasePlugin
from lib.conf.config import settings
from log.log_factory import error_logger


class BasicPlugin(BasePlugin.BasePlugin):

    def process(self, host, executor, response):
        try:
            if settings.TEST_MODE:
                with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/basic.txt', 'r') as f:
                    content = f.read()
                response.data = self.parse(content)
                return response.dict

            content = executor(host, 'echo "hostname: $(hostname) | os_platform: $(grep PRETTY_NAME /etc/os-release | cut -d'"' -f2) | os_version: $(grep VERSION_ID /etc/os-release | cut -d'"' -f2)"')
            response.data = self.parse(content)
        except Exception:
            error_logger.error(traceback.format_exc())
            response.status = False
            response.error = traceback.format_exc()
        return response.dict

    @staticmethod
    def parse(content):
        """
                解析shell命令返回结果
                :param content: shell 命令结果
                :return:解析后的结果
                """
        response = {}
        for item in content.split('|'):
            item = item.strip()
            key, value = item.split(':')
            response[key] = value

        return response
