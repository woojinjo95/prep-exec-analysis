import logging
from typing import List

import numpy as np

from .summary_info import SummaryInfo


logger = logging.getLogger('main_logger')


class CrackDiscriminator:

    def __init__(self, crack_score_thld: float,
                continuity_set_interval: int, continuity_hold_interval: int,
                crack_patch_ratio: float, row_crack_patch_ratio: float):
        # set params
        self.crack_score_thld = crack_score_thld
        self.continuity_set_interval = continuity_set_interval
        self.continuity_hold_interval = continuity_hold_interval
        self.crack_patch_ratio = crack_patch_ratio
        self.row_crack_patch_ratio = row_crack_patch_ratio
        logger.info(f'CrackDiscriminator. crack_score_thld={crack_score_thld}, continuity_set_interval={continuity_set_interval}, continuity_hold_interval={continuity_hold_interval}, crack_patch_ratio={crack_patch_ratio}, row_crack_patch_ratio={row_crack_patch_ratio}')

        self.crack_summary_info = SummaryInfo()

        # set variables
        self.frame_index = -1
        self.is_crack = False
        self.is_crack_cont = False
        self.crack_cont_mat = None
        self.crack_matrix = None

    def set_params(self, row_num: int, col_num: int, source_video_fps: float):
        self.row_num = row_num  # fix param (not dynamic)
        self.col_num = col_num  # fix param (not dynamic)

        self.source_video_fps = source_video_fps  # dynamic param
        self.continuity_set_thld = max(int(self.continuity_set_interval / 1000 * source_video_fps), 1)  # dynamic param
        self.continuity_hold_thld = max(int(self.continuity_hold_interval / 1000 * source_video_fps), 1)  # dynamic param

    def init_matrices(self, row_num: int, col_num: int):
        self.crack_cont_mat = np.zeros((row_num, col_num), np.int32)
        self.non_crack_cont_mat = np.zeros((row_num, col_num), np.int32)
        self.crack_patch_thld = max(int(row_num * col_num * self.crack_patch_ratio), 1)
        self.row_crack_patch_thld = max(int(col_num * self.row_crack_patch_ratio), 1)

    def get_binary_matrix(self, score_mat: np.ndarray) -> np.ndarray:
        det_mat = np.where(score_mat >= self.crack_score_thld, 1, 0).astype(np.int32)
        return det_mat

    def update_continuity_matrix(self, det_mat: np.ndarray, crack_cont_mat: np.ndarray, non_crack_cont_mat: np.ndarray, continuity_hold_thld: int):
        non_crack_cont_mat[det_mat == 0] += 1
        non_crack_cont_mat[det_mat == 1] = 0
        crack_cont_mat[det_mat == 1] += 1
        crack_cont_mat[non_crack_cont_mat >= continuity_hold_thld] = 0
        return crack_cont_mat, non_crack_cont_mat

    def is_rows_cracked(self, crack_matrix, row_crack_patch_threshold):
        det_rows = np.zeros((len(crack_matrix), 1), np.int32)
        for i, crack_matrix_row in enumerate(crack_matrix):
            if np.count_nonzero(crack_matrix_row) >= row_crack_patch_threshold:
                det_rows[i] = 1
        return det_rows

    def is_cracked(self, crack_matrix, crack_patch_threshold):
        return np.count_nonzero(crack_matrix) >= crack_patch_threshold

    def update_crack_status(self, scores):
        self.score_mat = np.reshape(scores, (self.row_num, self.col_num))  # score_mat: 각 패치 영역의 점수 matrix (2차원)
        self.det_mat = self.get_binary_matrix(self.score_mat)  # det_mat: 현재 프레임의 각 패치 영역이 깨졌는지에 대한 binary matrix

        if np.count_nonzero(self.det_mat) > 0:
            self.is_crack = True  # 현재 프레임의 패치가 하나라도 깨진 경우
        else:
            self.is_crack = False

        if self.crack_cont_mat is None:  # 초기화 작업
            self.init_matrices(self.row_num, self.col_num)

        self.crack_cont_mat, self.non_crack_cont_mat = self.update_continuity_matrix(  # crack_cont_mat: 깨짐 연속성 상태에 대한 matrix
            self.det_mat, self.crack_cont_mat, self.non_crack_cont_mat, self.continuity_hold_thld)

        # crack_matrix: 연속성 threshold에 의해 최종적으로 깨졌다고 판단된 binary matrix
        self.crack_matrix = self.crack_cont_mat >= self.continuity_set_thld
        # crack_cont_matrix: is_crack_cont 활성화시에만 crack_matrix와 같은 형태로 그려지는 matrix. 조건 불만족시 전부 0
        self.crack_cont_matrix = np.zeros_like(self.crack_matrix, dtype=self.crack_matrix.dtype)

        detection_rows = self.is_rows_cracked(self.crack_matrix, self.row_crack_patch_thld)
        if np.count_nonzero(detection_rows >= 1):  # row patch 비율 조건
            self.is_crack_cont = True  # is_crack_cont: 최종적으로 깨졌다고 판단된 경우
            self.crack_cont_matrix = self.crack_matrix.copy()
            return
        if self.is_cracked(self.crack_matrix, self.crack_patch_thld):  # 전체 patch 비율 조건
            self.is_crack_cont = True
            self.crack_cont_matrix = self.crack_matrix.copy()
            return

        self.is_crack_cont = False
        return

    def update(self, scores: List[float], row_num: int, col_num: int, send_fps: float, send_time: float) -> bool:
        self.set_params(row_num, col_num, send_fps)

        self.frame_index += 1
        self.update_crack_status(scores)
        self.crack_summary_info.update(self.is_crack_cont, self.frame_index, send_time)
        
    def get_summary(self) -> dict:
        summary = {
            'error_infos': self.crack_summary_info.error_infos,  # 에러 정보 리스트
            'error_state': self.crack_summary_info.error_flag  # 현재 에러 발생 중 여부
        }
        return summary
