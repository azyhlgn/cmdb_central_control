from src.plugins import get_server_info


def get_host_list():
    # 需要改成从API接口获得从数据库得到的当天未收集资产的hostlist
    host_list = ['192.168.22.129']
    return host_list


def run():
    host_list = get_host_list()
    for host in host_list:
        get_server_info(host)


if __name__ == '__main__':
    run()
