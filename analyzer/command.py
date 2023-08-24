from typing import Dict
import logging

from scripts.modules.color_reference import ColorReference
from scripts.modules.freeze_detect import FreezeDetect
from scripts.modules.warm_boot import WarmBoot
from scripts.modules.cold_boot import ColdBoot
from scripts.modules.log_level import LogLevel


logger = logging.getLogger('main')


class CommandExecutor:
    def __init__(self):
        self.color_ref_module = ColorReference()
        self.freeze_detect_module = FreezeDetect()
        self.warm_boot_module = WarmBoot()
        self.cold_boot_module = ColdBoot()
        self.log_level_module = LogLevel()

    def execute(self, command: Dict):
        # freeze_detect start:  PUBLISH command '{"msg": "analysis", "data": {"measurement": ["freeze"]}}'

        # if command.get('msg') == 'color_reference':
        #     arg = command.get('data', {})
        #     logger.info(f'msg: color_reference. arg: {arg}')

        #     control = arg.get('control', '')
        #     if control == 'start':
        #         self.color_ref_module.start()
        #     elif control == 'stop':
        #         self.color_ref_module.stop()
        #     else:
        #         logger.warning(f'Unknown control: {control}')
        
        if command.get('msg') == 'analysis':
            data = command.get('data', {})
            logger.info(f'msg: analysis. data: {data}')

            measurement = data.get('measurement', [])
            if 'freeze' in measurement:
                self.freeze_detect_module.start()
            if 'resume' in measurement:
                self.warm_boot_module.start()
            if 'boot' in measurement:
                self.cold_boot_module.start()
            if 'log_level_finder' in measurement:
                self.log_level_module.start()

        else:
            pass
