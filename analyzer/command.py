from typing import Dict
import logging
import queue
import time
import threading

from scripts.processor.freeze_detect import test_freeze_detection
from scripts.processor.warm_boot import test_warm_boot
from scripts.processor.cold_boot import test_cold_boot
from scripts.processor.log_pattern import test_log_pattern_matching
from scripts.processor.color_reference import test_color_reference
from scripts.format import Command


logger = logging.getLogger('main')


class CommandManager:
    def __init__(self, queue: queue.Queue):
        self.queue = queue

    def register(self, command: Dict):
        if command.get('msg') == 'analysis':  # 분석 명령
            self.queue.put(command)
            logger.info(f'put command: {command}. wait commands: {self.queue.qsize()}')
        # PUBLISH command '{"msg": "service_state", "data": {"state": "analysis"}}'
        elif command.get('msg') == 'service_state':  # 서비스 상태 변경 명령
            data = command.get('data', {})
            state = data.get('state', '')
            if state == 'analysis':  # 분석 모드 진입
                logger.info(f'enter analysis mode. wait commands: {self.queue.qsize()}')
                # color reference 테스트 작업을 분석 명령으로서 큐에 등록
                self.put_color_reference(command)

    def put_color_reference(self, command: Dict):
        command['msg'] = 'analysis'
        command['data'] = {'measurement': ['color_reference']}
        self.queue.put(command)


class CommandExecutor(threading.Thread):
    def __init__(self, queue: queue.Queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            time.sleep(1)
            command = self.queue.get()
            self.execute(command)

    def execute(self, command: Dict):
        # PUBLISH command '{"msg": "analysis", "data": {"measurement": ["freeze"]}}'
        logger.info(f'execute command: {command}. wait commands: {self.queue.qsize()}')

        data = command.get('data', {})
        logger.info(f'msg: analysis. data: {data}')

        measurement = data.get('measurement', [])
        if Command.COLOR_REFERENCE.value in measurement:
            test_color_reference()
        if Command.FREEZE.value in measurement:
            test_freeze_detection()
        if Command.RESUME.value in measurement:
            test_warm_boot()
        if Command.BOOT.value in measurement:
            test_cold_boot()
        if Command.LOG_PATTERN_MATCHING.value in measurement:
            test_log_pattern_matching()

