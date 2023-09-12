import serial
import time
from scripts.device.remocon.types.bluetooth.bt_constant import Commands

MEDIA_KEY_MAX = 0xFF07
MEDEA_KEY_MIN = 0x00

# basic utility functions
def open_ble_keyboard(port='COM8', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS):
    ser = serial.Serial(port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize)
    return ser


def _write_commands(ser, command, args):
    cmd_str = command + ",".join(args) + "\n"
    print(cmd_str, end="")
    ser.write(bytes(cmd_str, 'utf-8'))

    
def _send_code_with_command(ser, cmd, key_code):
    if -1 < key_code < 256:
        _write_commands(ser, cmd, [str(key_code)])
    else:
        print(f"invalid key_code: {key_code}")
    
    
def _send_media_code_with_command(ser, cmd, key_code):
    if isinstance(key_code, int) and MEDEA_KEY_MIN < key_code < MEDIA_KEY_MAX:
        _write_commands(ser, cmd, [hex(key_code)])
    else:
        print(f"invalid code type:{key_code}")

# function commands
def start(ser):
    _write_commands(ser, Commands.start, [])


def stop(ser):
    _write_commands(ser, Commands.stop, [])


def write(ser, key_code):
    cmd = Commands.write_key_code
    _send_code_with_command(ser, cmd, key_code)


def write_char(ser, key_char):
    cmd = Commands.write_key_code
    if(isinstance(key_char, str) and len(key_char) == 1):
        _send_code_with_command(ser, cmd, ord(key_char))
    else:
        print("invalid string")


def write_media(ser, key_code):
    cmd = Commands.write_media_key_code
    _send_media_code_with_command(ser, cmd, key_code)


def press(ser, key_code):
    cmd = Commands.press_key_code
    _send_code_with_command(ser, cmd, key_code)


def press_media_key(ser, key_code):
    cmd = Commands.press_media_key_code
    _send_media_code_with_command(ser, cmd, key_code)
    

def press_consumer_key(ser, key_code):
    _write_commands(ser, Commands.write_media_key_code, [str(key_code)])


def release(ser, key_code):
    cmd = Commands.release_key_code
    _send_code_with_command(ser, cmd, key_code)


def release_media(ser, key_code):
    cmd = Commands.release_media_key_code
    _send_code_with_command(ser, cmd, key_code)


def release_all(ser):
    _write_commands(ser, Commands.release_all, [])


def set_delay(ser, delay_ms):
    _write_commands(ser, Commands.set_delay, [str(delay_ms)])


def set_device_name(ser, device_name):
    _write_commands(ser, Commands.set_device_name, [str(device_name)])


def get_device_name(ser):
    _write_commands(ser, Commands.get_device_name, [])


def get_device_type(ser):
    _write_commands(ser, Commands.get_device_type, [])


def disconnect(ser):
    _write_commands(ser, Commands.disconnect, [])


def get_device_status(ser):
    _write_commands(ser, Commands.get_device_status, [])


# simple utilities -> keyboard key에 대해서만 가능함.
# media long press, media repeat가 추가 되어야 함.
# long press는 나중에 생각해야 하나?
def long_press(ser, key_code, duration):
    # TODO: 여기에 duration에 관한 제약사항 정리 하기 integer, 10 - 10000ms 사이? -> 제약 사항 있어야 함.
    _write_commands(ser, Commands.long_press, [str(key_code), str(duration)])


def long_press_media(ser, key_code, duration):
    press_media_key(ser, key_code)
    time.sleep(duration)
    release_media(ser, key_code)


def repeat(ser, key_code, interval, repeat_num):
    # TODO: 여기에 interval과 repeat_num에 대한 제약 사항 정리
    _write_commands(ser, Commands.long_press, [str(key_code), str(interval), str(repeat_num)])


def repeat_media(ser, key_code, interval, repeat_num):
    # TODO: 여기에 interval과 repeat_num에 대한 제약 사항 정리
    for i in range(repeat_num-1):
        write_media(ser, key_code)
        time.sleep(interval/1000)
    write_media(ser, key_code)


def write_string(ser, txt):
    # TODO: 여기에 txt에 대한 제약사항을 정리 할 필요 있음 길이. 10이하로.
    _write_commands(ser, Commands.write_string, [str(ord(c)) for c in txt])