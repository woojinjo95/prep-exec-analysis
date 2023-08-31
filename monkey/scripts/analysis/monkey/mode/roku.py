from ..intelligent_monkey_test import IntelligentMonkeyTest


class IntelligentMonkeyTestRoku(IntelligentMonkeyTest):
    def __init__(self):
        pass
    
    def get_cursor(self) -> Tuple:
        return find_roku_cursor(self.get_current_image())

    def check_leftmenu_is_opened(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, max_height_diff: int=10) -> bool:
        if cursor is None:
            return False
        else:
            height_diff = abs(cursor[3] - self.root_cursor[3])
            is_height_similar = height_diff < max_height_diff

            is_cursor_same = self.check_cursor_is_same(prev_image, prev_cursor, image, cursor)
            
            return True if is_height_similar and not is_cursor_same else False