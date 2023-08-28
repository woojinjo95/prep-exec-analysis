# -*- coding: utf-8 -*-
import time


def get_info():
    info =f'''[Unit]
Description=Bluetooth Arduino Cli
After=network-online.target

[Service]
RemainAfterExit=no
Type=simple
ExecStartPre=/usr/bin/sleep 30
ExecStart=/usr/bin/python3 /etc/bluetooth_service/bluetooth_auto_start.py

[Install]
WantedBy=default.target
    '''
    with open('bluetooth-remocon.service', 'w') as service_file:
        service_file.write(info)
    service_file.close()
    time.sleep(2) # 파일 생성시간 고려, 대기 시간 추가


if __name__=='__main__':
    get_info()