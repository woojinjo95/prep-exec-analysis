import time


class SummaryInfo:

    def __init__(self):
        self.error_infos = []
        self.error_flag = False

    # 연속된 status를 하나로 묶어서 레포팅
    def update(self, is_error_status, frame_index):
        if is_error_status:
            if not self.error_flag:
                self.error_infos.append({
                    'start_frame_index': frame_index,
                    'end_frame_index': frame_index,
                    'start_time': time.time(),
                    'end_time': time.time(),
                })
                self.error_flag = True

            self.error_infos[-1]['end_frame_index'] = frame_index
            self.error_infos[-1]['end_time'] = time.time()
            
        else:
            self.error_flag = False
