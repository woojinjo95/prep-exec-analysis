from typing import Tuple
import time
import ipaddress


class LCDStrings:
    # only one function string arg allowd

    def error_code(self, error_code: str) -> Tuple[str]:
        # 에러 코드 표시
        return (f'lc021:0,[ERROR_{error_code}]', )

    def uptime(self, uptime_seconds: float = None) -> Tuple[str]:
        # uptime

        if uptime_seconds // 3600 > 100:
            hour, minute, second = 99, 59, 59
        else:
            hour = uptime_seconds // 3600
            minute = (uptime_seconds % 3600) // 60
            second = uptime_seconds % 60

        return (f'lc021:0,{hour}h {minute}m {second}s', )

    def ir_state(self, state: str = 'on') -> Tuple[str]:
        # 리모컨 수단 ir
        if state == 'on':
            return ('lc011:1,0xFFFFFF', )
        else:
            # off
            return ('lc011:1,0x2F3237', )

    def bt_state(self, state: str = 'paired') -> Tuple[str]:
        # 리모컨 수단 bt
        if state == 'paired':
            return ('lc011:2,0x00FF00', )
        elif state == 'unpaired':
            return ('lc011:2,0xFF0000', )
        else:
            # off
            return ('lc011:2,0x2F3237', )

    def set_status(self, string: str = 'Ready') -> Tuple[str]:
        # 상태 Ready 표시
        # Ready
        # Check Connection
        # Analysing
        # Collecting
        return (f'lc021:3,{string}', )

    def wan_ip(self, ip_address: str) -> Tuple[str]:
        # WAN 초록색 설정 및 IP 주소 설정
        if ipaddress.ip_address(ip_address):
            return ('lc011:4,0x00FF00', f'lc021:7,{ip_address}')
        else:
            # WAN 빨간색 설정 및 UNKNOWN
            return ('lc011:4,0xFF0000', 'lc021:7,UNKNOWN')

    def stb_ip(self, ip_address: str) -> Tuple[str]:
        # WAN 초록색 설정 및 IP 주소 설정
        if ipaddress.ip_address(ip_address):
            return ('lc011:5,0x00FF00', f'lc021:8,{ip_address}')
        else:
            # WAN 빨간색 설정 및 UNKNOWN
            return ('lc011:5,0xFF0000', 'lc021:8,UNKNOWN')

    def video_input_state(self, state: str = 'on') -> Tuple[str]:
        # WAN 초록색 설정 및 UNKNOWN
        if state == 'on':
            return ('lc011:6,0x00FF00', )
        else:
            # WAN 빨간색 설정 및 UNKNOWN
            return ('lc011:6,0xFF0000', )

    def cpu_temp(self, value: str) -> Tuple[str]:
        value = int(value)
        # temp 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            return (f'lc021:12,{value}', f'lc031:9,{value}', 'lc011:9,0x2196F3')
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            return (f'lc021:12,{value}', f'lc031:9,{value}', 'lc011:9,0xFF9800')
        else:
            if value > 99:
                value = 99
            # Danger range : 71 ~ 100
            return (f'lc021:12,{value}', f'lc031:9,{value}', 'lc011:9,0xE91E63')

    def memory_usage(self, value: str) -> Tuple[str]:
        value = int(value)
        # ram 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            return (f'lc021:13,{value}', f'lc031:10,{value}', 'lc011:10,0x2196F3')
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            return (f'lc021:13,{value}', f'lc031:10,{value}', 'lc011:10,0xFF9800')
        else:
            # Danger range : 71 ~ 100
            return (f'lc021:13,{value}', f'lc031:10,{value}', 'lc011:10,0xE91E63')

    def ssd_uage(self, value: str) -> Tuple[str]:
        value = int(value)
        # ssd 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            return (f'lc021:14,{value}', f'lc031:11,{value}', 'lc011:11,0x2196F3')
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            return (f'lc021:14,{value}', f'lc031:11,{value}', 'lc011:11,0xFF9800')
        else:
            # Danger range : 71 ~ 100
            return (f'lc021:14,{value}', f'lc031:11,{value}', 'lc011:11,0xE91E63')
