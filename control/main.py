import logging

from scripts.configs.constant import RedisChannel, RemoconSetting
from scripts.configs.default import init_configs
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection)
from scripts.device.remocon.remocon_process import RemoconProcess
from scripts.device.serial.serial_device import (SerialDevice,
                                                 initial_serial_devices)
from scripts.device.serial_control import init_dut_state, change_dut_state
from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


@handle_errors
def init(serial_device: SerialDevice, remocon_process: RemoconProcess):
    # TODO change it to first loaded remocon id
    power_state, hdmi_state, wan_state = init_dut_state(serial_device)
    remocon_id = RemoconSetting.default_remocon_id
    remocon_process.set_remocon_id(remocon_id)
    logger.info(f'Init first state: vac: {power_state} / hpd: {hdmi_state} / lan: {wan_state} / remocon_id: {remocon_id}')


@handle_errors
def command_parser(command: dict, serial_device: SerialDevice, remocon_process: RemoconProcess):
    if command.get('remocon'):
        remocon_args = command.get('remocon')
        key = remocon_args.get('key')
        remocon_type = remocon_args.get('type', 'ir')
        press_time = remocon_args.get('press_time', 0)
        remocon_id = remocon_args.get('id')

        if remocon_id is not None and remocon_id != remocon_process.remocon_id_pointer.value:
            remocon_process.set_remocon_id(int(remocon_id))

        remocon_process.put_command(key=key, _type=remocon_type, press_time=press_time)

    if command.get('remocon_model'):
        remocon_type_args = command.get('remocon_model')
        remocon_id = remocon_type_args.get('id')
        remocon_process.set_remocon_id(int(remocon_id))

    if command.get('on_off_control'):
        on_off_control_args = command.get('on_off_control')
        change_dut_state(serial_device, on_off_control_args)
        

@handle_errors
def main():
    serial_devices = initial_serial_devices()
    control_board_serial_device = serial_devices.control
    remocon_process = RemoconProcess(serial_devices)

    init(control_board_serial_device, remocon_process)

    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command, control_board_serial_device, remocon_process)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer()
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('remocon', 1)
        log_organizer.set_stream_logger('serial', 6)
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start control container')

        init_configs()
        main()

    finally:
        logger.info('Close control container')
        log_organizer.close()
