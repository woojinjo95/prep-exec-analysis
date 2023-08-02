import os
import paramiko
import subprocess
import logging
from ..utils.docker import is_running_in_docker
from ..configs.redis_connection import hget_single

# from ..configs.config import get_setting


static_root_path = os.path.join('/app', 'static')
rsa_key_path = os.path.join(static_root_path, 'keys', 'runner_key')

HOST = 'host.docker.internal'
USER = os.environ.get('USER', 'nextlab')
PORT = hget_single('hardware_configuration', 'ssh_port', 2345, 0)
TIMEOUT = 3

logger = logging.getLogger('connection')


def run_command_in_docker_host(command: str, ip: str = HOST, username: str = USER, port: int = PORT, timeout: float = TIMEOUT) -> str:
    output = ''
    if is_running_in_docker():
        logger.info(f'This command; "{command}" is need to run on host computer, self-ssh command is executed')
        try:
            with paramiko.SSHClient() as client:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                public_key = paramiko.RSAKey.from_private_key_file(rsa_key_path)
                client.connect(ip, username=username, port=port, timeout=timeout, pkey=public_key)
                _, stdout, stderr = client.exec_command(command)

                output = stdout.read().decode("utf-8").strip() if stdout is not None else ''
                error = stderr.read().decode("utf-8").strip() if stderr is not None else ''
                if error:
                    logger.warning(f'Error in executing command by host ssh: {error}')
        except paramiko.AuthenticationException:
            logger.critical(f"Failed to connect to {ip}: Authentication failed! Check file in OS")
        except paramiko.SSHException as sshex:
            logger.error(f"Failed to connect to {ip}: {sshex}")
        except Exception as ex:
            logger.error(f"Failed to connect to {ip}: {ex}")
        finally:
            return output
    else:
        logger.info(f'This command; "{command}" is need to be executed on host computer, and current program is not in docker container.')
        try:
            output = subprocess.check_output(command, shell=True)
        except:
            pass
