import os
import glob


def start_arduino_cli():
    path = os.path.join(os.environ["HOME"], 'projects', 'prep-exec-analysis', 'bluetooth_service')
    pattern = os.path.join(path, 'bluetooth_keyboard_esp32s3*')
    folder = glob.glob(pattern)
    os.system(f'./arduino-cli compile -b esp32:esp32:esp32s3 {folder[0]}/ -p /dev/ttyUSB0 && echo "Bluetooth Compile 완료"')
    os.system(f'./arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32s3:UploadSpeed=115200 {folder[0]}/ && echo "Bluetooth Upload 완료"')
    

if __name__ == '__main__':
    start_arduino_cli()