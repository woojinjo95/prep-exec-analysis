
import traceback
def check_skip_message(message: any):
    try:
        level = message.pop('level')
        # info가 아닌 모든 메시지 스킵
        if level != 'info':
            return False

        # msg가 shell이 아닌 모든 메시지 스킵
        msg = message.pop('msg')
        if msg != 'shell':
            return False

        # 에코 메시지 스킵 (혹시 몰라서)
        msg = message.pop('service')
        if msg == 'shell':
            return False
        return True
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False

