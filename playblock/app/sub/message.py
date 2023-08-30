
import json
import traceback
from datetime import datetime 

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


class COMMAND:
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


def check_skip_message(raw: any):
    try:
        if raw is None:
            return False, None
        if not isinstance(raw, dict):
            return False, None

        message = json.loads(raw['data'])

        # 에코 메시지 체크
        service = message['service']
        if service == 'shell':
            print(f"check_skip_message service == {service}")
            return False, None

        level = message['level']
        # info가 아닌 모든 메시지 스킵
        if level != 'info':
            print(f"check_skip_message level: {level}")
            print(f"trace: {message}")
            return False, None

        # msg가 start or stop이 아닌 모든 메시지 스킵
        # msg = message['msg']
        # if msg != 'start' and msg != 'stop':
        #     print(f"check_skip_message shell: {msg}")
        #     return False, None

        # data = message['data']
        # if data is None:
        #     print(f"check_skip_message data: {data}")
        #     return False

        return True, message
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False, None


if __name__ == "__main__":
    msg1 = COMMAND("a service", "a level", "a msg", "a data")

    print(msg1.to_json())
    print(msg1)

    msg2 = COMMAND("a service", "a level", "a msg", {"data": "a asdfsdfsdf", "number": 12322})
    print(msg2.to_json())
    print(msg2)