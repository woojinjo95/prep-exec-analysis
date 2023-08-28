
import traceback


def check_skip_message(message: any, shell_id: int):
    try:
        # 에코 메시지 체크
        service = message.get('service')
        if service == 'shell':
            print(f"check_skip_message service == {service}")
            return False

        level = message.get('level')
        # info가 아닌 모든 메시지 스킵
        if level != 'info':
            print(f"check_skip_message level: {level}")
            print(f"trace: {message}")
            return False

        # msg가 shell이 아닌 모든 메시지 스킵
        msg = message.get('msg')
        if msg != 'shell':
            print(f"check_skip_message shell: {msg}")
            return False

        data = message.get('data')
        if data is None:
            print(f"check_skip_message data: {data}")
            return False

        # 쉘 아이디 비교
        id = data.get('shell_id')
        if id is None:
            print(f"check_skip_message id: {id}")
            return False
        if id != shell_id:
            print(f"check_skip_message shell_id != {id}")
            return False

        return True
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False
