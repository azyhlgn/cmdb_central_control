from src.plugins import BasePlugin
from lib.executor.paramiko_executor import paramiko_executor

from config import setting


class CpuPlugin(BasePlugin.BasePlugin):

    def process(self,host):

        if setting.TEST_MODE:
            with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/cpu.txt', 'r') as f:

                content = f.read()
            return self.parse(content)

        content = paramiko_executor(host,'cat /proc/cpuinfo')
        return self.parse(content)

    @staticmethod
    def parse(content):
        """
                解析shell命令返回结果
                :param content: shell 命令结果
                :return:解析后的结果
                """
        response = {'cpu_count': 0, 'cpu_physical_count': 0, 'cpu_model': ''}

        cpu_physical_set = set()

        content = content.strip()
        for item in content.split('\n\n'):
            for row_line in item.split('\n'):
                key, value = row_line.split(':')
                key = key.strip()
                if key == 'processor':
                    response['cpu_count'] += 1
                elif key == 'physical id':
                    cpu_physical_set.add(value)
                elif key == 'model name':
                    if not response['cpu_model']:
                        response['cpu_model'] = value
        response['cpu_physical_count'] = len(cpu_physical_set)

        print(response)

        return response


