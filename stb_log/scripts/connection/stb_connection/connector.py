import io
import logging
import os
import time
from threading import Event
from iterators import TimeoutIterator

import paramiko
from ppadb.client import Client as AdbClient

logger = logging.getLogger('connection')


class Connection:
    def __init__(self, host: str, port: int, username: str = None, password: str = None, connection_mode: str = 'ssh'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection_mode = connection_mode
        if connection_mode == 'ssh':
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.client.connect(host, port=port, username=username, password=password, timeout=2)
        elif connection_mode == 'adb':
            os.system('adb start-server')
            self.client = AdbClient(host="127.0.0.1", port=5037)
            self.client.remote_connect(host, int(port))
            self.device = self.client.device(f"{host}:{port}")
            self.session = self.create_connection(timeout=2)
            if self.session is None:
                raise Exception('Invalid IP or Port')
        else:
            raise Exception('Invalid connection_mode')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection_mode == 'ssh':
            if self.client:
                self.client.close()
        elif self.connection_mode == 'adb':
            if self.session:
                self.session.close()

    def create_connection(self, timeout: float = 2) -> any:
        start_time = time.time()
        # time out을 설정하고, create_connection에 성공할 때 까지 계속 시도
        while True:
            try:
                time.sleep(0.1)
                return self.device.create_connection()
            except Exception as e:
                if time.time() - start_time >= timeout:
                    return None

    def preprocess_stdout_stream(self, stdout: io.TextIOWrapper, stop_event: Event):
        while not stop_event.is_set():
            try:
                line = stdout.readline()
                if line == "":
                    break
                yield line
            except Exception as e:
                line = ""
                while True:
                    try:
                        if self.connection_mode == "adb":
                            x = stdout.read(1).encode()
                        else:
                            x = stdout.read(1)
                    except Exception as e:
                        continue
                    line += x.decode()
                    if x == b"\n":
                        yield line
                        break

        # logger.info('stdout stop_event set')
        if self.connection_mode == 'ssh':
            self.client.close()
        elif self.connection_mode == 'adb':
            stdout.close()
            if self.session:
                self.session.close()
        del stdout

    def exec_command(self, command: str, stop_event: Event):
        if self.connection_mode == 'ssh':
            stdin, stdout, stderr = self.client.exec_command(command)
        elif self.connection_mode == 'adb':
            cmd = "shell:{}".format(command)
            self.session.send(cmd)
            stdout = self.session.socket.makefile()
        return self.preprocess_stdout_stream(stdout, stop_event)
