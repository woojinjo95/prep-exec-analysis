from typing import Tuple
import time


class LCDStrings:
    # only one function arg allowd

    def error_code(self, error_code: int) -> Tuple[str]:
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

    def ir_on(self) -> Tuple[str]:
        # 리모컨 수단 ir
        return ('lc011:1,0xFFFFFF', )

    def ir_off(self) -> Tuple[str]:
        # 리모컨 수단 ir
        return ('lc011:1,0x2F3237', )

    def bt_off(self) -> Tuple[str]:
        # 리모컨 수단 bt
        return ('lc011:2,0x2F3237', )

    def bt_unpaired(self) -> Tuple[str]:
        # 리모컨 수단 bt
        return ('lc011:2,0xFF0000', )

    def bt_paired(self) -> Tuple[str]:
        # 리모컨 수단 bt
        return ('lc011:2,0x00FF00', )

    def status_ready(self) -> Tuple[str]:
        # 상태 Ready 표시
        return ('lc021:3,Ready', )

    def status_check_connection(self) -> Tuple[str]:
        # 상태 Check Connection 표시
        return ('lc021:3,Check Connection', )

    def status_analysing(self) -> Tuple[str]:
        # 상태 Analysing 표시
        return ('lc021:3,Analysing', )

    def status_collecting(self) -> Tuple[str]:
        # 상태 Collecting 표시
        return ('lc021:3,Collecting', )

    def wan_ip(self, ip_address: str) -> Tuple[str]:
        # WAN 초록색 설정 및 IP 주소 설정
        return ('lc011:4,0x00FF00', f'lc021:7,{ip_address}')

    def wan_fail(self) -> Tuple[str]:
        # WAN 빨간색 설정 및 UNKNOWN
        return ('lc011:4,0xFF0000', 'lc021:7,UNKNOWN')

    def stb_ip(self, ip_address: str) -> Tuple[str]:
        # WAN 초록색 설정 및 IP 주소 설정
        return ('lc011:5,0x00FF00', f'lc021:8,{ip_address}')

    def stb_fail(self) -> Tuple[str]:
        # WAN 빨간색 설정 및 UNKNOWN
        return ('lc011:5,0xFF0000', 'lc021:8,UNKNOWN')

    def video_input_success(self) -> Tuple[str]:
        # WAN 초록색 설정 및 UNKNOWN
        return ('lc011:6,0x00FF00', )

    def video_intput_fail(self) -> Tuple[str]:
        # WAN 빨간색 설정 및 UNKNOWN
        return ('lc011:6,0xFF0000', )

    def temp(self, value: int) -> Tuple[str]:
        # temp 설정
        if 0 < value <= 50:
            # Safe range : 0 ~ 50
            return (f'lc021:12,{value}', f'lc031:9,{value}', 'lc011:9,0x2196F3')
        elif 50 < value <= 70:
            # Caution range : 51 ~ 70
            return (f'lc021:12,{value}', f'lc031:9,{value}', 'lc011:9,0xFF9800')
        else:
            # Danger range : 71 ~ 100
            return (f'lc021:12,{value}', f'lc031:9,{value}', 'lc011:9,0xE91E63')

    def ram(self, value: int) -> Tuple[str]:
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

    def ssd(self, value: int) -> Tuple[str]:
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
