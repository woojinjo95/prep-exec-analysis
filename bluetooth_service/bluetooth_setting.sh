# /Emerald & Garent Linix

# 먼저 athana-runner-renewal 폴더 내 bluetooth zip파일이 존재해야 한다.
# 경로는 향후 변경 작업 진행
# 신규 장비가 linux server 이기 때문에 세부 경로는 변경될 수 있음
cd /home/$USER/projects/prep-exec-analysis/bluetooth_service/
unzip bluetooth_keyboard_esp32s3_ver05.zip && rm bluetooth_keyboard_esp32s3_ver05.zip

cd bluetooth_keyboard_esp32s3_ver05/
python get_device_name.py

cd ..

curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/home/$USER/projects/prep-exec-analysis/bluetooth_service/ sh

./arduino-cli config init --overwrite

cd /home/$USER/.arduino15/

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
cd /home/$USER/projects/prep-exec-analysis/bluetooth_service/
./arduino-cli core update-index
./arduino-cli core install esp32:esp32

./arduino-cli compile -b esp32:esp32:esp32s3 bluetooth_keyboard_esp32s3_ver05/ -p /dev/ttyUSB0 && echo "Compile를 완료했습니다."
./arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32s3:UploadSpeed=115200 bluetooth_keyboard_esp32s3_ver05/ && echo "Upload를 완료했습니다."

# ./arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=115200     # 모니터링 필요 시 사용

cd /etc
sudo mkdir -v bluetooth_service

cd /home/$USER/projects/prep-exec-analysis/bluetooth_service/
python bluetooth_register_service.py

sudo mv -f bluetooth_auto_start.py /etc/bluetooth_service
sudo mv -f BluetoothRemocon.service /etc/systemd/system
sudo systemctl enable BluetoothRemocon.service
sudo systemctl start BluetoothRemocon.service
sudo systemctl status BluetoothRemocon

