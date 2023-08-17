from typing import Dict
import logging

from scripts.modules.color_reference import ColorReference
from scripts.modules.freeze_detect import FreezeDetect


logger = logging.getLogger('main')


class CommandExecutor:
    def __init__(self):
        self.color_ref_module = ColorReference()
        self.freeze_detect_module = FreezeDetect()

    # Color Reference
    def start_color_ref_module(self):
        self.color_ref_module.start()
    
    def stop_color_ref_module(self):
        self.color_ref_module.stop()

    # Freeze Detect
    def start_freeze_detect_module(self):
        self.freeze_detect_module.start()
    
    def stop_freeze_detect_module(self):
        self.freeze_detect_module.stop()

    def execute(self, command: Dict):
        # color_reference start:  PUBLISH command '{"msg": "color_reference", "data": {"control": "start"}}'
        # color_reference stop:  PUBLISH command '{"msg": "color_reference", "data": {"control": "stop"}}'

        # freeze_detect start:  PUBLISH command '{"msg": "freeze_detect", "data": {"control": "start"}}'
        # freeze_detect stop:  PUBLISH command '{"msg": "freeze_detect", "data": {"control": "stop"}}'

        if command.get('msg') == 'color_reference':
            arg = command.get('data', {})
            logger.info(f'msg: color_reference. arg: {arg}')

            control = arg.get('control', '')
            if control == 'start':
                self.start_color_ref_module()
            elif control == 'stop':
                self.stop_color_ref_module()
            else:
                logger.warning(f'Unknown control: {control}')
        
        elif command.get('msg') == 'freeze_detect':
            arg = command.get('data', {})
            logger.info(f'msg: freeze_detect. arg: {arg}')

            control = arg.get('control', '')
            if control == 'start':
                self.start_freeze_detect_module()
            elif control == 'stop':
                self.stop_freeze_detect_module()
            else:
                logger.warning(f'Unknown control: {control}')

        else:
            pass
