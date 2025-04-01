from src.plugins.BasePlugin import BasePlugin
from lib.conf.config import settings


class DiskPlugin(BasePlugin):

    def process(self, host, executor):
        if settings.TEST_MODE:
            with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/disk.txt', 'r') as f:
                content = f.read()
            return self.parse(content)

        content = executor(host, 'MegaCli -PDList -aAll')
        return self.parse(content)

    @staticmethod
    def parse(content):
        response = {}
        devices = []
        key_map = {
            'Slot Number': 'slot',
            'RAW Size': 'capacity',
            'Inquiry Data': 'model',
            'PD Type': 'pd_type'
        }

        for device in content.split("\n\n"):
            if device.startswith('Adapter'):
                continue
            devices.append(device)

        for device in devices:
            temp_dict = {}
            for row in device.split('\n'):
                if len(row.split(':')) == 2:
                    row_data = row.split(':')
                    if row_data[0] in key_map:
                        temp_dict[key_map[row_data[0]]] = row_data[1].strip()

            if temp_dict:
                response[temp_dict['slot']] = temp_dict

        print(response)
        return response
