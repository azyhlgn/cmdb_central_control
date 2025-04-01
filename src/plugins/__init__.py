import importlib
import traceback

from lib.conf.config import settings
from log.log_factory import error_logger


def get_server_info(host=None):
    for key, value in settings.PLUGINS_DICT.items():
        module = importlib.import_module(value)
        plugin_obj = getattr(module, key)()
        executor_path = settings.EXECUTOR_DICT[settings.EXECUTOR_MODE]
        executor_name = executor_path.rsplit('.', maxsplit=1)[-1]
        executor_module = importlib.import_module(executor_path)
        executor = getattr(executor_module, executor_name)
        try:
            data = plugin_obj.process(host, executor)
        except Exception:
            error_logger.error(traceback.format_exc())
