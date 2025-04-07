import re
import traceback
import json
from src.plugins import BasePlugin
from lib.conf.config import settings
from log.log_factory import error_logger

class NicPlugin(BasePlugin.BasePlugin):
    test_mode = True

    def process(self, host, executor, response):
        try:
            if settings.TEST_MODE:
                content = []
                with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/nic_link.txt', 'r') as f:
                    content.append(f.read())
                with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/nic_addr.txt', 'r') as f:
                    content.append(f.read())

                content = '\n'.join(content)
                response.data = self.parse(content)
                return response.dict

            content = [executor(host, 'ip -o link show'), executor(host, 'ip -o addr show')]
            content = '\n'.join(content)
            response.data = self.parse(content)
            return response.dict

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
        # TODO 需要修改一下 适配数据库的数据结构

        for line in content.splitlines():
            line = line.strip()

            # 逐行分析ip -o link show 命令结果
            if "link/ether" in line or "link/loopback" in line:
                # 按space分割部分
                parts = re.split(r'\s+', line)
                if_name = parts[1].replace(':', '')
                mac = parts[parts.index('brd') - 1] if 'link/ether' in line else None
                state = parts[parts.index('state') + 1]

                current_nic = {
                    "name": if_name,
                    "hwaddr": mac,
                    'ipaddrs_netmask': {},
                    "up": state,
                }
                response[if_name] = current_nic

            # 逐行分析ip -o addr show 命令结果
            elif "inet" in line:
                parts = re.split(r'\s+', line)
                if_name = parts[1]
                ip_family = "ipv6" if "inet6" in line else "ipv4"
                ip_cidr = parts[3]

                # 关联到当前网卡
                for nic in response.keys():
                    if nic == if_name:
                        response[nic]['ipaddrs_netmask'][ip_family] = ip_cidr
                        break
        print(json.dumps(response))
        return response
