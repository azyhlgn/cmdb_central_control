import os
import sys
import traceback
# import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests

os.environ['USER_SETTINGS'] = 'config.settings'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.conf.config import settings
from src.plugins import get_server_info

thread_pool = ThreadPoolExecutor(max_workers=5)


def get_host_list():
    # if settings.TEST_MODE:
    #
    #     # 需要改成从API接口获得从数据库得到的当天未收集资产的hostlist
    #     host_list = ['192.168.22.129']
    #     return host_list

    host_list = requests.get(settings.API_ASSET_URL)
    return host_list.json()


def run():
    host_list = get_host_list()
    for host in host_list:
        thread_pool.submit(get_server_info, host)


if __name__ == '__main__':

    if settings.EXECUTOR_MODE == 'agent':
        get_server_info()

    run()
