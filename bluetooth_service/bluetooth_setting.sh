# /Emerald & Garent Linix

# 먼저 athana-runner-renewal 폴더 내 bluetooth zip파일이 존재해야 한다.
# 경로는 향후 변경 작업 진행
# 신규 장비가 linux server 이기 때문에 세부 경로는 변경될 수 있음

pip install esptool

cd $HOME/projects/prep-exec-analysis/bluetooth_service/
unzip bluetooth_keyboard_esp32s3_*.zip && rm bluetooth_keyboard_esp32s3_*.zip

cd bluetooth_keyboard_esp32s3_*/
python3 get_device_name.py

cd ..

curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/home/$USER/projects/prep-exec-analysis/bluetooth_service/ sh

./arduino-cli config init --overwrite

cd $HOME/.arduino15/

yaml_file="$HOME/.arduino15/arduino-cli.yaml"
address='https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json'
line_number=$(grep -n 'additional_urls:' $yaml_file | cut -d ':' -f 1)
if [ -n "$line_number" ]; then
    sed -i "${line_number}s|.*|  additional_urls: [\"$address\"]|" $yaml_file
    echo "주소가 추가되었습니다."
else
    echo "additional_urls 키를 찾을 수 없습니다."
fi
# 경로는 향후 변경 작업 진행
cd $HOME/projects/prep-exec-analysis/bluetooth_service/
./arduino-cli core update-index
./arduino-cli core install esp32:esp32

./arduino-cli compile -b esp32:esp32:esp32s3 bluetooth_keyboard_esp32s3_ver05/ -p /dev/ttyUSB0 -e

bin_path=$HOME/projects/prep-exec-analysis/bluetooth_service/bluetooth_keyboard_esp32s3_ver05/build/esp32.esp32.esp32s3  # 경로 주의

python3 "$HOME/.arduino15/packages/esp32/tools/esptool_py/4.5.1/esptool.py" --chip esp32s3 --port "/dev/ttyUSB0" --baud 115200  --before default_reset --after hard_reset write_flash -e -z --flash_mode dio --flash_freq 80m --flash_size 4MB 0x0 "$bin_path/bluetooth_keyboard_esp32s3_ver05.ino.bootloader.bin" 0x8000 "$bin_path/bluetooth_keyboard_esp32s3_ver05.ino.partitions.bin" 0xe000 "$HOME/.arduino15/packages/esp32/hardware/esp32/2.0.11/tools/partitions/boot_app0.bin" 0x10000 "$bin_path/bluetooth_keyboard_esp32s3_ver05.ino.bin" && echo "Upload success"

# ./arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=115200     # 모니터링 필요 시 사용

cd /etc
sudo mkdir -p bluetooth_service

cd $HOME/projects/prep-exec-analysis/bluetooth_service/
python3 bluetooth_register_service.py

sudo mv -f bluetooth_auto_start.py /etc/bluetooth_service
sudo mv -f bluetooth-remocon.service /etc/systemd/system
sudo systemctl enable bluetooth-remocon.service
sudo systemctl start bluetooth-remocon.service
sudo systemctl status bluetooth-remocon

