import importlib
import traceback

from config.setting import PLUGINS_DICT
from log.log_factory import error_logger


def get_server_info(host):
    for key, value in PLUGINS_DICT.items():
        module = importlib.import_module(value)
        plugin_obj = getattr(module, key)()
        try:
            data = plugin_obj.process(host)
        except Exception:
            error_logger.error(traceback.format_exc())
