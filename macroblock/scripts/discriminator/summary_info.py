import time


class SummaryInfo:

    def __init__(self):
        self.__now_start_frame_index = None
        self.__now_start_time = None
        self.__error_infos = []
        self.error_flag = False

    @property
    def error_infos(self):
        return self.__error_infos

    # 연속된 status를 하나로 묶어서 레포팅
    def update(self, is_error_status, frame_index, send_time):
        if is_error_status:
            if not self.error_flag:
                self.__now_start_time = send_time
                self.__now_start_frame_index = frame_index
                self.__error_infos.append({})
                self.error_flag = True

            now_error_info = {
                'time': self.__now_start_time,
                'duration': send_time - self.__now_start_time,
                'start_frame_index': self.__now_start_frame_index,
                'end_frame_index': frame_index
            }
            self.__error_infos[-1] = now_error_info

        else:
            self.error_flag = False
