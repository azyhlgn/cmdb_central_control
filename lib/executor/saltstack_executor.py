from salt import client

from lib.conf.config import settings


def saltstack_executor(host, command):
    local = client.LocalClient()
    result = local.cmd(host, 'cmd.run', command)

    return result.decode(settings.EXECUTOR_ENCODING)
