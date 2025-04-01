import subprocess
# from lib.conf.config import settings


def agent_executor(host,command):
    # subprocess的返回值已经经过了decode
    result = subprocess.getoutput(command)
    return result

