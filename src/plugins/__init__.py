import importlib
import traceback
import json
import requests
import pprint

from lib.conf.config import settings
from log.log_factory import error_logger
from lib.response.BaseResponse import BaseResponse


def import_string(dotted_path):
    module_path, class_name = dotted_path.rsplit('.', maxsplit=1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_server_info(host=None):
    data_dict = {}

    # 获得处理机
    executor_path = settings.EXECUTOR_DICT[settings.EXECUTOR_MODE]
    executor = import_string(executor_path)

    for key, value in settings.PLUGINS_DICT.items():
        # 字符串导入插件 并且实例化
        plugin_obj = import_string(value)()

        try:
            data_dict[key] = plugin_obj.process(host, executor, BaseResponse())
        except Exception:
            error_logger.error(traceback.format_exc())

    print(json.dumps(data_dict))

    ret = requests.post(
        settings.API_ASSET_URL,
        json=json.dumps(data_dict),
        headers={'Content-Type': 'application/json'},
    )
    print(ret.text)

    # # 放入事件循环
    # try:
    #     task_list.append(plugin_obj.process(host, executor))
    # except Exception as e:
    #     print(e)

    # try:
    #     # 在主线程中，调用get_event_loop总能返回属于主线程的event loop对象
    #     # 如果是处于非主线程中，还需要调用set_event_loop方法指定一个event loop对象
    #     # 这样get_event_loop才会获取到被标记的event loop对象
    #     thread_loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(thread_loop)
    #     # 异步启动
    #     loop = asyncio.get_event_loop()
    #     # run_until_complete本身就类似一个await
    #     loop.run_until_complete(asyncio.gather(*task_list))
    # except Exception as e:
    #     error_logger.error(traceback.format_exc())
