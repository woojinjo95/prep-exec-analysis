import multiprocessing
import time
import queue
import logging
from typing import Dict, Callable, Tuple, List

from scripts.format import Command
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

        self.processes = {}  # 모든 동작 중 프로세스. key: pid, value: process
        self.cmd_queue = multiprocessing.Queue()

        if self.mode == "sync":
            self.start_command_executor()

    def register(self, command: Dict):
        logger.info(f'register command: {command}')
        # parse to module function and args
        exec_list = self.parse_command(command)
        for func, args in exec_list:
            logger.info(f'execute: {func.__name__}({args})')
            if self.mode == "sync":
                self.cmd_queue.put((func, args))
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

    ##### Command Consumer #####
    def start_command_executor(self):
        proc = multiprocessing.Process(target=self.command_executor)
        proc.start()

    def command_executor(self):
        while True:
            try:
                func, args = self.cmd_queue.get_nowait()
                proc = self.start_process(func, args)
                proc.join()
            except queue.Empty:
                time.sleep(1)

    ##### Process Control #####
    def start_process(self, func: Callable, args: Tuple) -> multiprocessing.Process:
        proc = multiprocessing.Process(target=func, args=args)
        proc.start()
        self.processes[proc.pid] = proc
        return proc

    def stop_processes(self):
        while not self.cmd_queue.empty():
            self.cmd_queue.get()
        for pid, process in self.processes.items():
            process.terminate()
            process.join()
        self.processes = {}

    def remove_process_by_id(self, pid):
        if pid in self.processes:
            self.processes[pid].terminate()
            self.processes[pid].join()
            del self.processes[pid]
