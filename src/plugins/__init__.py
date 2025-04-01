import importlib
import traceback

from lib.conf.config import settings
from log.log_factory import error_logger


def get_server_info(host):
    for key, value in settings.PLUGINS_DICT.items():
        module = importlib.import_module(value)
        plugin_obj = getattr(module, key)()
        executor_path,executor_name = settings.EXECUTOR_MODE.rsplit('.',maxsplit=1)
        executor_module = importlib.import_module(settings.EXECUTOR_MODE)
        executor = getattr(executor_module, executor_name)
        print(type(executor))
        try:
            data = plugin_obj.process(host,executor)
        except Exception:
            error_logger.error(traceback.format_exc())
