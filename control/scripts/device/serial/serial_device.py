import logging
import time
import serial
import re
from multiprocessing import Lock, Manager
from typing import List, Tuple

from .control_board import set_packet, trans_data, trans_start, trans_end, get_hex, repeat_ir, led_state, counter_set
from .ir_constant import Status, IrFrame
from ...configs.config import get_value

use_control_board = True

logger = logging.getLogger('serial')


class SerialDevice:
    def __init__(self, serial_port: str, baud_rate: int = 115200):
        """_summary_
        Args:
            serial_port (str): serial port for serial device
            baud_rate (int, optional): baud rate for serial transmission
        """
        self.lock = Lock()  # lock with current serial port
        self.serial_port = Manager().Value('c', serial_port)
        self.baud_rate = baud_rate
        self.end_transmit = IrFrame.start
        self.last_pronto_code = None
        self.time_offset = 0.004
        self.use_control_board = True

        # init packet
        self.prev_packet = Manager().dict()
        self.prev_packet['status'] = 'ready'
        self.prev_packet['irbtrcv'] = 'irbton'
        self.prev_packet['hpd'] = 'on'
        self.prev_packet['lan'] = 'on'
        self.prev_packet['vac'] = 'on'
        if self.use_control_board:
            self.set_packet(status='ready', irbtrcv='irbton', hpd='on', lan='on', vac='on')  # set default state

    def set_serial_port(self, serial_port: str):
        self.serial_port.value = serial_port

    # 시리얼 제어
    def write(self, hex_string: str):
        """_summary_
        hex string을 그대로 전송
        Args:
            hex_string (str): aa010300000101010001ee
        """
        with self.lock, serial.Serial(self.serial_port.value, self.baud_rate, timeout=1) as ser:
            byte_data = bytes.fromhex(hex_string)
            ser.write(byte_data)

    # LED 제어
    def construct_led_code(self, state: str) -> List[str]:
        """_summary_
        construct hex strings of LED control with state
        Args:
            state (str): state defined in 'Status.status_list'
                -> ['ready' | 'network' | 'start' | 'finish' | 'findme' | 'found' | 'poweroff']
        Returns:
            hex_strings (List[str]): strings contained [0-f] 
                -> ['03000000000003ffff', '03000000000003ffff', ... ]
        """
        state = state.lower()
        led_state_list = Status.status_list
        if state in led_state_list:
            value = led_state_list.index(state) + 1
            hex_strings = led_state(setting=value)
            return hex_strings

    def set_led(self, state: str) -> None:
        """_summary_
        control LED with state
        Args:
            state (str): state defined in 'Status.status_list'
                -> ['ready' | 'network' | 'start' | 'finish' | 'findme' | 'found' | 'poweroff']
        LED function tests can be performed, but other functions may be turned off due to signal configuration
        """
        hex_strings = self.construct_led_code(state)
        self.transmit(hex_strings)

    # 리모콘 제어
    def construct_ir_code(self, pronto_code: str, repeat_number: int = 0) -> List[str]:
        """_summary_
        construct hex strings of IR control with pronto code
        Args:
            pronto_code (str): pronto code
                -> '0000 006E 0022 0002... '
            repeat_number (int, optional): repeat number. Defaults to 0.
        Returns:
            hex_strings (List[str]): strings contained [0-f] 
                -> ['03000000000003ffff', '03000000000003ffff', ... ]
        """
        codes = pronto_code.split()
        length = len(codes)
        hex_len = get_hex(length)
        hex_strings = []
        hex_strings.append(trans_start(length=hex_len))

        for raw_index, raw_code in enumerate(codes):
            values = ''.join([get_hex(ord(c)) for c in raw_code][::-1])
            index = get_hex(raw_index + 1)
            hex_strings.append(trans_data(value=values, index_2=index))
        hex_strings.append(trans_end())
        hex_strings.append(repeat_ir(repeat_num=repeat_number))
        return hex_strings

    def transmit(self, hex_strings: List[str], press_time: float = 0, serial_get_event_time: bool = False) -> Tuple[bool, any]:
        """_summary_
        write hex strings to serial device
        Args:
            hex_strings (List[str]): strings contained [0-f] and added prefix and postfix
                -> ['03000000000003ffff', '03000000000003ffff', ... ]
            press_time: (float): long press time.
            get_event_time (bool, optional): return event time
        Returns:
            Tuple[bool, any]: (success of fail, start time of writing) 
        """
        timeout = press_time + 0.25 if press_time > 0 else 0.096  # 0.108 freq and add some padding
        if not self.use_control_board:
            transform_hex_strings = []
            if type(hex_strings) == list:
                for hex in hex_strings:
                    transform_hex_strings.append(f'aa{hex}ee')
                    time.sleep(0.015)
                hex_strings = transform_hex_strings
            else:
                hex_strings = [f'aa{hex_strings}ee']
        else:
            hex_strings = [f'aa{hex}ee' for hex in hex_strings] if type(hex_strings) == list else [f'aa{hex_strings}ee']
            hex_strings = self.counter_setting('reset') + self.counter_setting('start') + hex_strings
        try:
            start_time = time.time()  # 혹시 모를 중복 선언임
            with self.lock, serial.Serial(self.serial_port.value, self.baud_rate, timeout=timeout) as ser:
                start_time = time.time()
                for hex_string in hex_strings:
                    byte_data = bytes.fromhex(hex_string)
                    ser.write(byte_data)
                if serial_get_event_time:
                    # reset, start, code, code end, transmit, start info, end_info -> 904 bytes
                    serial_len = 11 * (2 + 76 + 1 + 1)  # + 20 bytes padding   -> 924 bytes
                    counter_hex = ser.read(serial_len)
                    while b'\xee\xaa\x15\x01\x00' not in counter_hex[:-5]:
                        counter_hex += ser.read(1)
                    transmit_time = self.cal_counter(counter_hex)
                    remocon_event_time = start_time + transmit_time + self.time_offset
                    return remocon_event_time
        except Exception as e:
            logger.debug(f'serial write raise error => {e}')
            remocon_event_time = start_time + 0.007
            if self.use_control_board:
                logger.error(f'Failed to parse value!! real value is in this range: {remocon_event_time} +- 0.001')
            return remocon_event_time

    def read_data(self, length: int = 80, timeout: int = 1) -> Tuple[bool, any]:
        """_summary_
        read hex strings from serial device
        Returns:
            hex_strings (List[str]): strings contained [0-f] and added prefix and postfix. first code is 1.
                -> b 'xaa x14 xcd0 xcc3 x00 x03 x00 x00 xee~'
        """
        try:
            with self.lock, serial.Serial(self.serial_port.value, self.baud_rate, timeout=timeout) as ser:
                data_line = ser.read(length)
            return True, data_line
        except Exception as e:
            logger.debug(f'read data error =>{e}')

    def transmit_ir(self, pronto_code: str, press_time: float = 0, serial_get_event_time: bool = False) -> float:
        """_summary_
        control remocon with pronto code
        Args:
            pronto_code (str): pronto code
                -> '0000 006E 0022 0002... '
            get_event_time (bool, optional): return event time or not
        Return:
            float: event time  
        """
        repeat_count = max(0, int(press_time // .108 - 1))  # ir 신호 repeat code 전송 주기 간격 : 108 ms
        if self.last_pronto_code != pronto_code:
            hex_strings = self.construct_ir_code(pronto_code, repeat_count)
        else:
            hex_strings = [repeat_ir(repeat_num=repeat_count)]
        event_time = self.transmit(hex_strings, press_time, serial_get_event_time)
        self.last_pronto_code = pronto_code
        return event_time

    # 기타 제어
    def set_packet(self, status: str = None, irbtrcv: str = None, hpd: str = None, lan: str = None, vac: str = None, log=True) -> None:
        """_summary_
        set control board with packet 
        Args:
            status (str): status   (LED 제어)
                -> 'ready' | 'network' | 'start' | 'finish' | 'findme' | 'found' | 'poweroff'
                -> ready: 장비 동작 중
                -> network: 네트워크 연결 가능 상태
                -> start: TC 시작
                -> finish: TC 종료
                -> findme: 장비 위치를 알려주며 깜빡이는 LED
                -> found: 장비를 찾았음
                -> poweroff: 장비 동작 중이지 않음 (이거는 장비가 애초에 꺼진 상태라서 LED도 안 나오므로 의미 없다고 함)
            irbtrcv (str): irbtrcv (IR, BT 제어)
                -> 'iron' | 'bton' | irbton' | 'irbtoff'
                -> iron: IR 제어 모드
                -> bton: Bluetooth 제어 모드
                -> irbton: IR / BT 동시 제어 모드
                -> irbtoff: IR / BT 제어 불가 모드
            hpd (str): hpd
                -> hdmi 제어
                -> 'on' | 'off',  default:'on'
            lan (str): lan         
                -> 인터넷 제어
                -> 'on' | 'off',  default:'on'
            vac (str): vac         
                -> 파워 제어
                -> 'on' | 'off',  default:'on'
        """

        # 입력된 값이 none일 때는 가장 최근 상태를 가져와야 함. -> 안 그러면 덮어쓰므로
        current_packet = {
            'status': self.prev_packet['status'] if not status else status,
            'irbtrcv': self.prev_packet['irbtrcv'] if not irbtrcv else irbtrcv,
            'hpd': self.prev_packet['hpd'] if not hpd else hpd,
            'lan': self.prev_packet['lan'] if not lan else lan,
            'vac': self.prev_packet['vac'] if not vac else vac
        }

        # set packet
        hex_string = set_packet(**current_packet)
        self.transmit(hex_string)
        if log:
            logger.info(f'set packet. prev: {self.prev_packet.copy()} -> current: {current_packet}')
        else:
            logger.debug(f'set packet. prev: {self.prev_packet.copy()} -> current: {current_packet}')

        # dump current to prev
        for key, value in current_packet.items():
            self.prev_packet[key] = value

    def counter_setting(self, control: str) -> str:
        """_summary_
        To initialize or Count start or Count reset the 1 ms cycle counter
        Args:
            control (str): counter state.  [ 'start' | 'stop' | 'reset' | 'request' ]
                -> request: counter return packet
        Return:
            str: hex strings    def counter_setting(self, control: str) -> any:
        """
        hex_strings = counter_set(control=control)
        hex_strings = [f'aa{hex}ee' for hex in hex_strings] if type(hex_strings) == list else [f'aa{hex_strings}ee']
        return hex_strings

    def cal_counter(self, counter_hexs: str) -> float:
        """_summary_
        Count the time after sending the remote control signal
        Args:
            counter_hexs (str): hex strings of list type
        Returns:
            float: calculated time
        """
        try:
            counter_hexs = bytes.hex(counter_hexs)
            lines = counter_hexs.split('ee')
            for line in lines[::-1]:
                start_calc = re.search(r'aa150100(?P<value>.{8})', line)
                if start_calc == None:
                    continue
                else:
                    counter_value_string = start_calc['value']
                    counter_calc = int(counter_value_string, 16) / 1000
                    return counter_calc
        except Exception as e:
            logger.debug(f'calc error =>{e}')


def initial_serial_devices() -> Tuple[SerialDevice, SerialDevice]:
    baud_rate = int(get_value('devices', 'serial_baud_rate'))
    ir_serial_port = get_value('devices', 'ir_remocon_port')
    bt_serial_port = get_value('devices', 'bt_remocon_port')
    ir_serial_device = SerialDevice(ir_serial_port, baud_rate=baud_rate)
    bt_serial_device = SerialDevice(bt_serial_port, baud_rate=baud_rate)
    serial_devices = (ir_serial_device, bt_serial_device)
    return serial_devices
