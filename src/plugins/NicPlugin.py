import re

from src.plugins import BasePlugin
from lib.executor.paramiko_executor import paramiko_executor
from config import setting


class NicPlugin(BasePlugin.BasePlugin):
    test_mode = True

    def process(self, host):
        if setting.TEST_MODE:
            content = []
            with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/nic_link.txt', 'r') as f:
                content.append(f.read())
            with open('/Users/zy/CMDB/CMDB_Central_Control/资产收集的示例返回值/nic_addr.txt', 'r') as f:
                content.append(f.read())

            content = '\n'.join(content)
            return self.parse(content)

        content = paramiko_executor(host, 'dmidecode -q -t 17 2>/dev/null')
        return self.parse(content)

    @staticmethod
    def parse(content):
        """
                解析shell命令返回结果
                :param content: shell 命令结果
                :return:解析后的结果
                """
        response = []

        for line in content.splitlines():
            line = line.strip()

            # 逐行分析ip -o link show 命令结果
            if "link/ether" in line or "link/loopback" in line:
                # 按space分割部分
                parts = re.split(r'\s+', line)
                if_name = parts[1].replace(':', '')
                mac = parts[parts.index('brd')-1] if 'link/ether' in line else None
                state = parts[parts.index('state')+1]
                mtu = parts[parts.index('mtu')+1].replace("mtu", "")

                current_nic = {
                    "name": if_name,
                    "mac": mac,
                    "state": state,
                    "mtu": mtu,
                    "ipv4": [],
                    "ipv6": []
                }
                response.append(current_nic)

            # 逐行分析ip -o addr show 命令结果
            elif "inet" in line:
                parts = re.split(r'\s+', line)
                if_name = parts[1]
                ip_family = "ipv6" if "inet6" in line else "ipv4"
                ip_cidr = parts[3]
                ip, cidr = ip_cidr.split('/') if '/' in ip_cidr else (ip_cidr, None)
                scope = parts[parts.index('scope')+1]

                # 关联到当前网卡
                for nic in response:
                    if nic["name"] == if_name:
                        nic[ip_family].append({
                            "address": ip,
                            "cidr": cidr,
                            "scope": scope
                        })
                        break

        print(response)
        return response


# NicPlugin().process("123")
