import paramiko
from lib.conf.config import settings

def paramiko_executor(host, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, settings.SSH_PORT, username=settings.SSH_USER,password=settings.SSH_PASSWORD)
    # 需要改成公钥私钥登陆

    stdin, stdout, stderr = ssh.exec_command(command)

    result = stdout.read()
    ssh.close()

    return result.decode(settings.EXECUTOR_ENCODING)
