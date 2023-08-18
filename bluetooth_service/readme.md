블루투스 사용 전 초기 세팅을 할 수 있습니다.

bluetooth_setting.sh 실행 시 기초 세팅이 완료됩니다.

명령어 : bash bluetooth_setting.sh      // sudo 사용금지

기초 세팅 정보
- 설치: arduino cli
- 보드: esp32s3
- port: /dev/ttyUSB0
- baudrate: 115200

내부 로직
1. bluetooth_keyboard_esp32s3_ver05 알집 해제
2. get_device_name.py를 실행해 device name을 가져옴 -> 블루투스 코드 실행 시 활용
3. arduino cli 의 기초 셋팅 및 보드 라이브러리 다운로드, 설치
4. 컴파일 및 업로드
5. 부팅 시 자동 컴파일 및 업로드 될 수 있도록 서비스 등록