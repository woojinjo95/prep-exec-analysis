from .file_manager import FileManager


class LogFileManager(FileManager):
    def __init__(self, session: Session):
        pass

    def dump(self, output_path: str):
        pass

    def load(self, start: float, end: float):
        pass

    def delete(self, start: float, end: float):
        pass

    