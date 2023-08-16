
from datetime import datetime 
import json
# 컨트롤 - 리모콘 - 블루투스 전환 
# DUT 파워 컨트롤
# HPD HDMI 파워컨트롤
# DUT WAN 파워 컨트롤 

# 네트워크 에뮬레이션 적용 /해제 (대역폭, 지연, 로스)
# 로그수집 디바이스 선택

# 터미널 추가 / 삭제
# 터미널 명령 송신

# 리모콘 명령 송신
# 리모콘 커스텀키 명령 송신


class Message:
    service: str
    level: str
    msg: str
    data: dict | str
    time: datetime

    def __init__(self, service: str, level: str, msg: str, data: dict | str):
        self.service = service
        self.level = level
        self.msg = msg
        self.data = data
        self.time = datetime.now()

    def __str__(self):
        return f"[{self.time}] {self.level} {self.service} {self.msg} {self.data}"

    def to_json(self):
        return json.dumps(self.__dict__, default=str)


if __name__ == "__main__":
    msg1 = Message("a service", "a level", "a msg", "a data")

    print(msg1.to_json())
    print(msg1)

    msg2 = Message("a service", "a level", "a msg", {"data": "a asdfsdfsdf", "number": 12322})
    print(msg2.to_json())
    print(msg2)