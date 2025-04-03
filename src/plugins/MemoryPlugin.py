import traceback

from src.plugins import BasePlugin
from lib.conf.config import settings
from log.log_factory import error_logger


class MemoryPlugin(BasePlugin.BasePlugin):

    def process(self, host, executor, response):
        try:
            if settings.TEST_MODE:
                with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/memory.txt', 'r') as f:
                    content = f.read()
                response.data = self.parse(content)
                return response.dict

            content = executor(host, 'dmidecode -q -t 17 2>/dev/null')
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
        key_map = {
            'Size': 'capacity',
            'Locator': 'slot',
            'Type': 'model',
            'Speed': 'speed',
            'Manufacturer': 'manufacturer',
            'Serial Number': 'sn',

        }
        devices = content.split('\n\n')

        for device in devices:
            temp_dict = {}
            for row in device.split('\n\t'):
                if len(row.split(':')) == 2:
                    row_data = row.split(':')
                    if row_data[0] in key_map:
                        temp_dict[key_map[row_data[0]]] = row_data[1].strip()

            if temp_dict:
                response[temp_dict['slot']] = temp_dict

        return response
