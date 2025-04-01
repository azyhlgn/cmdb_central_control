import paramiko

def paramiko_executor(host, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, username='root',password='root')
    # 需要改成公钥私钥登陆

    stdin, stdout, stderr = ssh.exec_command(command)

    result = stdout.read()
    ssh.close()

    return result.decode('utf-8')


print(dir())
print([name for name in dir() if name.endswith('s__')])