- 아두이노에 다음의 환경설정 적용
https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json,https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_dev_index.json
- 설치 펌웨어는 esp32s3 dev module  
- 사용 포트는 0또는 1인데 s와 S로 명령내릴때 응답이 있는 종류 boudrate는 115200

아두이노를 통한 compile 및 upload 시 device 계정명이 필요함. 
get_device_name.py를 실행해 device 계정명을 가져와야 한다.

