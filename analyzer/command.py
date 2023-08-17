from typing import Dict
import logging

from scripts.modules.color_reference import ColorReference


logger = logging.getLogger('main')


class CommandExecutor:
    def __init__(self):
        self.color_ref_module = ColorReference()

    def start_color_ref_module(self):
        self.color_ref_module.start()
    
    def stop_color_ref_module(self):
        self.color_ref_module.stop()

    def execute(self, command: Dict):
        # color_reference start:  PUBLISH command '{"msg": "color_reference", "data": {"control": "start"}}'
        # color_reference stop:  PUBLISH command '{"msg": "color_reference", "data": {"control": "stop"}}'

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
