import multiprocessing
import time
import logging
import psutil
import traceback
import json
from typing import Dict, Callable, Tuple, List

from scripts.format import Command
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.processor.freeze_detect import test_freeze_detection
from scripts.processor.warm_boot import test_warm_boot
from scripts.processor.cold_boot import test_cold_boot
from scripts.processor.log_pattern import test_log_pattern_matching
from scripts.processor.color_reference import test_color_reference

logger = logging.getLogger('main')


class AnalysisManager:
    def __init__(self, mode: str):
        self.mode = mode  # sync | async
        logger.info(f'analysis mode: {self.mode}')

        self.storage = RedisStorage()

        if self.mode == "sync":
            self.start_command_executor()

    ##### Command Producer #####
    def register(self, command: Dict):
        logger.info(f'register command: {command}')
        # parse to module function and args
        exec_list = self.parse_command(command)
        for func, args in exec_list:
            logger.info(f'execute: {func.__name__}{args}')
            if self.mode == "sync":
                self.storage.enqueue_command(func, args)
            else:
                self.start_process(func, args)

    def parse_command(self, command: Dict) -> List[Tuple[Callable, Tuple]]:
        exec_list = []

        # PUBLISH command '{"msg": "analysis", "data": {"measurement": ["freeze"]}}'
        if command.get('msg') == 'analysis':  # 분석 명령
            data = command.get('data', {})
            measurement = data.get('measurement', [])
            if Command.COLOR_REFERENCE.value in measurement:
                exec_list.append((test_color_reference, ()))
            if Command.FREEZE.value in measurement:
                exec_list.append((test_freeze_detection, ()))
            if Command.RESUME.value in measurement:
                exec_list.append((test_warm_boot, ()))
            if Command.BOOT.value in measurement:
                exec_list.append((test_cold_boot, ()))
            if Command.LOG_PATTERN_MATCHING.value in measurement:
                exec_list.append((test_log_pattern_matching, ()))

        # PUBLISH command '{"msg": "service_state", "data": {"state": "analysis"}}'
        elif command.get('msg') == 'service_state':  # 서비스 상태 변경 명령
            data = command.get('data', {})
            state = data.get('state', '')
            if state == 'analysis':  # 분석 모드 진입
                exec_list.append((test_color_reference, ()))
        
        return exec_list

    ##### Command Consumer #####
    def start_command_executor(self):
        def command_executor():
            while True:
                time.sleep(1)
                command = self.storage.dequeue_command()
                if command:
                    func, args = command
                    proc = self.start_process(func, args)
                    proc.join()
                else:
                    pass

        proc = multiprocessing.Process(target=command_executor)
        proc.start()

    ##### Process Control #####
    def start_process(self, func: Callable, args: Tuple) -> multiprocessing.Process:
        proc = multiprocessing.Process(target=func, args=args)
        proc.start()
        self.storage.store_process(proc.pid, {'func': func.__name__, 'args': args})
        logger.info(f'start process: {proc.pid}')
        return proc

    def stop_processes(self):
        self.storage.empty_command_queue()
        self.storage.terminate_all_processes()
        logger.info('stop all processes')

    def remove_process_by_id(self, pid):
        self.storage.remove_process(pid)


class RedisStorage:
    def __init__(self):
        self.client = get_strict_redis_connection()
        self.processes_name = "processes"
        self.cmd_queue_name = "cmd_queue"
        
    def store_process(self, pid: int, metadata: Dict={}):
        self.client.hset(self.processes_name, pid, json.dumps(metadata))

    def terminate_all_processes(self):
        all_pids = self.client.hkeys(self.processes_name)
        for pid in all_pids:
            pid = int(pid.decode('utf-8'))
            self.remove_process(pid)
        self.client.delete(self.processes_name)

    def remove_process(self, pid: int):
        try:
            process = psutil.Process(pid)
            process.terminate()
        except psutil.NoSuchProcess:
            logger.warning(f"Process with PID {pid} not found.")
        self.client.hdel(self.processes_name, pid)

    def enqueue_command(self, func: Callable, args: Tuple):
        command = json.dumps({'func_name': func.__name__, 'args': args})
        self.client.lpush(self.cmd_queue_name, command)
        logger.info(f'command queue length: {self.command_length()}')

    def dequeue_command(self) -> Tuple[Callable, Tuple]:
        try:
            command_byte = self.client.rpop(self.cmd_queue_name)
            if command_byte:
                command = json.loads(command_byte)
                # func_name to func that is defined in this module
                func_name = command.get('func_name')
                func = globals().get(func_name)
                args = command.get('args')
                return func, args
            else:
                return None
        except Exception as e:
            logger.error(f'Error in dequeue_command: {e}')
            logger.warning(traceback.format_exc())
            return None

    def command_length(self) -> int:
        return self.client.llen(self.cmd_queue_name)

    def empty_command_queue(self):
        while self.client.llen(self.cmd_queue_name) > 0:
            self.client.rpop(self.cmd_queue_name)
