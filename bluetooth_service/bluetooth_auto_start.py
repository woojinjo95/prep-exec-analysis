import os
import glob


def start_arduino_cli():
    path = os.path.join(os.environ["HOME"], 'projects', 'prep-exec-analysis', 'bluetooth_service')
    pattern = os.path.join(path, 'bluetooth_keyboard_esp32s3*', 'build', 'esp32.esp32.esp32s3')
    folder = glob.glob(pattern)
    os.system(f'python3 "$HOME/.arduino15/packages/esp32/tools/esptool_py/4.5.1/esptool.py" --chip esp32s3 --port "/dev/ttyUSB0" --baud 115200  --before default_reset --after hard_reset write_flash -e -z --flash_mode dio --flash_freq 80m --flash_size 4MB 0x0 "{folder[0]}/bluetooth_keyboard_esp32s3_ver05.ino.bootloader.bin" 0x8000 "{folder[0]}/bluetooth_keyboard_esp32s3_ver05.ino.partitions.bin" 0xe000 "$HOME/.arduino15/packages/esp32/hardware/esp32/2.0.11/tools/partitions/boot_app0.bin" 0x10000 "{folder[0]}/bluetooth_keyboard_esp32s3_ver05.ino.bin"&& echo "Bluetooth Upload 완료"')
    

if __name__ == '__main__':
    start_arduino_cli()