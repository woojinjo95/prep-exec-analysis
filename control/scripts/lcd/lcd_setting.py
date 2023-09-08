import serial


class LCDSetting:
    def __init__(self, serial):
        self.serial = serial

    # serial
    def open_lcd(self, port='COM8', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS):
        self.serial = serial.Serial(port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize)

    def error_code(self, error_code: int) -> None:
        # 에러 코드 표시
        self.serial.write(bytes(f'lc021:0,[ERROR_{error_code}]', 'utf-8'))

    def uptime(self, hour: int, minute: int, second: int) -> None:
        # uptime 시간 표시
        # uptime = '18h 28m 31s' format
        self.serial.write(bytes(f'lc021:0,{hour}h {minute}m {second}s', 'utf-8'))

    def ir_on(self) -> None:
        # 리모컨 수단 ir
        self.serial.write(bytes(f'lc011:1,0xFFFFFF', 'utf-8'))

    def ir_off(self) -> None:
        # 리모컨 수단 ir
        self.serial.write(bytes(f'lc011:1,0x2F3237', 'utf-8'))

    def bt_off(self) -> None:
        # 리모컨 수단 bt
        self.serial.write(bytes(f'lc011:2,0x2F3237', 'utf-8'))

    def bt_unpaired(self) -> None:
        # 리모컨 수단 bt
        self.serial.write(bytes(f'lc011:2,0xFF0000', 'utf-8'))

    def bt_paired(self) -> None:
        # 리모컨 수단 bt
        self.serial.write(bytes(f'lc011:2,0x00FF00', 'utf-8'))

    def status_ready(self) -> None:
        # 상태 Ready 표시
        self.serial.write(bytes(f'lc021:3,Ready', 'utf-8'))

    def status_check_connection(self) -> None:
        # 상태 Check Connection 표시
        self.serial.write(bytes(f'lc021:3,Check Connection', 'utf-8'))

    def status_analysing(self) -> None:
        # 상태 Analysing 표시
        self.serial.write(bytes(f'lc021:3,Analysing', 'utf-8'))

    def status_collecting(self) -> None:
        # 상태 Collecting 표시
        self.serial.write(bytes(f'lc021:3,Collecting', 'utf-8'))

    def wan_ip(self, ip_address: str) -> None:
        # WAN 초록색 설정 및 IP 주소 설정
        self.serial.write(bytes(f'lc011:4,0x00FF00', 'utf-8'))
        self.serial.write(bytes(f'lc021:7,{ip_address}', 'utf-8'))

    def wan_fail(self) -> None:
        # WAN 빨간색 설정 및 UNKNOWN
        self.serial.write(bytes(f'lc011:4,0xFF0000', 'utf-8'))
        self.serial.write(bytes(f'lc021:7,UNKNOWN', 'utf-8'))

    def stb_ip(self, ip_address: str) -> None:
        # WAN 초록색 설정 및 IP 주소 설정
        self.serial.write(bytes(f'lc011:5,0x00FF00', 'utf-8'))
        self.serial.write(bytes(f'lc021:8,{ip_address}', 'utf-8'))

    def stb_fail(self) -> None:
        # WAN 빨간색 설정 및 UNKNOWN
        self.serial.write(bytes(f'lc011:5,0xFF0000', 'utf-8'))
        self.serial.write(bytes(f'lc021:8,UNKNOWN', 'utf-8'))

    def video_input_success(self) -> None:
        # WAN 초록색 설정 및 UNKNOWN
        self.serial.write(bytes(f'lc011:6,0x00FF00', 'utf-8'))

    def video_intput_fail(self) -> None:
        # WAN 빨간색 설정 및 UNKNOWN
        self.serial.write(bytes(f'lc011:6,0xFF0000', 'utf-8'))

    def temp(self, value: int) -> None:
        # temp 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            self.serial.write(bytes(f'lc021:12,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:9,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:9,0x2196F3', 'utf-8'))
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            self.serial.write(bytes(f'lc021:12,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:9,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:9,0xFF9800', 'utf-8'))
        else:
            # Danger range : 71 ~ 100
            self.serial.write(bytes(f'lc021:12,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:9,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:9,0xE91E63', 'utf-8'))

    def ram(self, value: int) -> None:
        # ram 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            self.serial.write(bytes(f'lc021:13,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:10,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:10,0x2196F3', 'utf-8'))
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            self.serial.write(bytes(f'lc021:13,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:10,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:10,0xFF9800', 'utf-8'))
        else:
            # Danger range : 71 ~ 100
            self.serial.write(bytes(f'lc021:13,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:10,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:10,0xE91E63', 'utf-8'))

    def ssd(self, value: int) -> None:
        # ssd 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            self.serial.write(bytes(f'lc021:14,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:11,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:11,0x2196F3', 'utf-8'))
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            self.serial.write(bytes(f'lc021:14,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:11,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:11,0xFF9800', 'utf-8'))
        else:
            # Danger range : 71 ~ 100
            self.serial.write(bytes(f'lc021:14,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc031:11,{value}', 'utf-8'))
            self.serial.write(bytes(f'lc011:11,0xE91E63', 'utf-8'))
