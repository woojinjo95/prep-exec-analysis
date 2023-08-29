import multiprocessing
import time
import logging
import threading
from queue import Queue
from typing import Dict, Callable, Tuple, List

from scripts.format import Command
from scripts.processor import (test_freeze_detection, test_warm_boot, test_cold_boot, test_log_pattern_matching, test_color_reference)

logger = logging.getLogger('main')


class AnalysisManager:
    def __init__(self, mode: str):
        self.mode = mode  # sync | async
        logger.info(f'analysis mode: {self.mode}')

        self.processes = {}  # pid: process
        self.process_info = {}  # pid: process info
        self.queue = Queue()

        if self.mode == "sync":
            self.start_command_executor()

    ##### Command Producer #####
    def register(self, command: Dict):
        exec_list = self.parse_command(command)
        for func, args in exec_list:
            logger.info(f'register: {func.__name__}{args}')
            if self.mode == "sync":
                self.queue.put((func, args))
                logger.info(f'queue size: {self.queue.qsize()}')
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
                func, args = self.queue.get()
                proc = self.start_process(func, args)
                proc.join()

        executor = threading.Thread(target=command_executor)
        executor.start()

    ##### Process Control #####
    def start_process(self, func: Callable, args: Tuple) -> multiprocessing.Process:
        logger.info(f'func: {func}, args: {args}')

        proc = multiprocessing.Process(target=func, args=args)
        proc.start()
        logger.info(f'started process: {proc.pid}')

        self.processes[proc.pid] = proc
        return proc

    def stop_processes(self):
        for pid, proc in self.processes.items():
            proc.terminate()
            logger.info(f'stopped process: {pid}')
        logger.info('stop all processes')
