import os
import importlib

from . import global_settings


class Settings():

    def __init__(self):
        # 获取默认配置参数并赋值
        for name in [name for name in dir(global_settings) if name.isupper()]:
            setattr(self, name, getattr(global_settings, name))

        # 获取自定义配置 并覆盖赋值
        module = importlib.import_module(os.environ.get('USER_SETTINGS'))
        for name in [name for name in dir(module) if name.isupper()]:
            setattr(self, name, getattr(module, name))


settings = Settings()