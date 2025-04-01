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

EXECUTOR_DICT = {
    'agent': 'lib.executor.agent_executor',
    'paramiko': 'lib.executor.paramiko_executor',
    'salt': 'lib.executor.saltstack_executor',
}

EXECUTOR_MODE = 'paramiko'

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s'

# 错误日志
ERROR_LOG_FILE = os.path.join(BASE_DIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASE_DIR, "log", 'run.log')


# SSH模式 参数
SSH_PORT = 22
SSH_USER = 'root'
SSH_PASSWORD = 'root'


# executor返回值编码格式
EXECUTOR_ENCODING = 'utf-8'
