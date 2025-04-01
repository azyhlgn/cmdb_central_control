import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEST_MODE = True

PLUGINS_DICT = {
    'DiskPlugin': 'src.plugins.DiskPlugin',
    'CpuPlugin': 'src.plugins.CpuPlugin',
    'MainBoardPlugin': 'src.plugins.MainBoardPlugin',
    'MemoryPlugin': 'src.plugins.MemoryPlugin',
    'NicPlugin': 'src.plugins.NicPlugin',
}

EXECUTOR_MODE = 'lib.executor.paramiko_executor'

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s'

# 错误日志
ERROR_LOG_FILE = os.path.join(BASE_DIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASE_DIR, "log", 'run.log')
