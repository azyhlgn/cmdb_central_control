from src.plugins.BasePlugin import BasePlugin
from lib.executor.paramiko_executor import paramiko_executor

from config import setting


class MainBoardPlugin(BasePlugin):

    def process(self, host):
        if setting.TEST_MODE:
            with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/mainboard.txt', 'r') as f:
                content = f.read()
            return self.parse(content)

        content = paramiko_executor(host, 'MegaCli -PDList -aAll')
        return self.parse(content)

    @staticmethod
    def parse(content):
        response = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }

        for item in content.split('\n\n'):
            if len(response) == 3:  # 在response中有完整信息后直接返回 不在继续分析多余数据
                break
            if item.startswith('#'):    # 排除第一块#开头的无用信息 增加解析效率
                continue

            for row in item.split('\n'):
                row_data = row.strip().split(':')
                # print(row_data)
                if len(row_data) == 2:
                    if row_data[0] in key_map:
                        response[key_map[row_data[0]]] = row_data[1].strip()

        print(response)
        return response
