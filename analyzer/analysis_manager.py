import multiprocessing
import time
import logging
import traceback
import json
from operator import attrgetter
import threading
import uuid
from typing import Dict, Callable, Tuple, List

from scripts.format import Command
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts import processor
from scripts.processor import (test_freeze_detection, test_warm_boot, test_cold_boot, test_log_pattern_matching, test_color_reference)

logger = logging.getLogger('main')


class AnalysisManager:
    def __init__(self, mode: str):
        self.mode = mode  # sync | async
        logger.info(f'analysis mode: {self.mode}')

        self.storage = RedisStorage()
        self.pool = multiprocessing.Pool()

        if self.mode == "sync":
            self.start_command_executor()

    def __del__(self):
        self.pool.close()
        self.pool.join()

    ##### Command Producer #####
    def register(self, command: Dict):
        # parse to module function and args
        exec_list = self.parse_command(command)
        for func, args in exec_list:
            logger.info(f'register: {func.__name__}{args}')
            if self.mode == "sync":
                self.storage.enqueue_command(func, args)
            elif self.mode == 'async':
                self.start_process(func, args)
            else:
                logger.error(f'invalid analysis mode: {self.mode}')

    def parse_command(self, command: Dict) -> List[Tuple[Callable, Tuple]]:
        exec_list = []

        # PUBLISH command '{"msg": "analysis", "data": {"measurement": ["freeze"]}}'
        if command.get('msg') == 'analysis':  # 분석 명령
            data = command.get('data', {})
            measurement = data.get('measurement', [])
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
                    async_result = self.start_process(func, args)
                    try:
                        result = async_result.get()
                    except Exception as e:
                        logger.error(f"Error executing function {func.__name__}: {e}")
                else:
                    pass

        executor = threading.Thread(target=command_executor)
        executor.start()

    ##### Process Control #####
    def start_process(self, func: Callable, args: Tuple):
        process_id = str(uuid.uuid4())
        logger.info(f'func: {func}, args: {args}')
        async_result = self.pool.apply_async(func, args=args, callback=lambda result: self.cleanup(process_id))
        self.storage.store_process(process_id, {'func': func.__name__, 'args': args})
        logger.info(f'started process: {process_id}')
        return async_result  # Note: returning the async result and not the process object
    
    def cleanup(self, process_id):
        self.storage.remove_process(process_id)
        logger.info(f'removed process: {process_id}')

    # def stop_processes(self):
    #     self.storage.empty_command_queue()
    #     self.storage.terminate_all_processes()
    #     logger.info('stop all processes')

    # def remove_process_by_id(self, pid):
    #     self.storage.remove_process(pid)


class RedisStorage:
    def __init__(self):
        self.client = get_strict_redis_connection()
        self.processes_name = "processes"
        self.cmd_queue_name = "cmd_queue"

        # init redis
        self.client.delete(self.processes_name)
        self.client.delete(self.cmd_queue_name)

    ##### Process Management #####
    def store_process(self, pid: int, metadata: Dict={}):
        self.client.hset(self.processes_name, pid, json.dumps(metadata))

    # def terminate_all_processes(self):
    #     for pid in self.get_all_pids():
    #         self.remove_process(pid)
    #     self.client.delete(self.processes_name)

    def remove_process(self, pid: int):
        self.client.hdel(self.processes_name, pid)

    # def get_all_pids(self) -> List[int]:
    #     all_pids = self.client.hkeys(self.processes_name)
    #     all_pids = [int(pid.decode('utf-8')) for pid in all_pids]
    #     return all_pids

    ##### Queue Management #####
    def enqueue_command(self, func: Callable, args: Tuple):
        command = json.dumps({'func_name': func.__name__, 'args': args})
        self.client.lpush(self.cmd_queue_name, command)
        logger.info(f'command queue length: {self.command_length()}')

    def dequeue_command(self) -> Tuple[Callable, Tuple]:
        try:
            command_byte = self.client.rpop(self.cmd_queue_name)
            if command_byte:
                command = json.loads(command_byte)
                func_name = command.get('func_name')
                # func_name to func that is defined in this module
                func = attrgetter(func_name)(processor)
                args = tuple(command.get('args'))
                return func, args
            else:
                return None
        except Exception as e:
            logger.error(f'Error in dequeue_command: {e}')
            logger.warning(traceback.format_exc())
            return None

    def command_length(self) -> int:
        return self.client.llen(self.cmd_queue_name)

    # def empty_command_queue(self):
    #     while self.client.llen(self.cmd_queue_name) > 0:
    #         self.client.rpop(self.cmd_queue_name)
