from abc import ABCMeta, abstractmethod


class FileManager(metaclass=ABCMeta):
    @abstractmethod
    def dump(self, output_path: str):
        pass

    @abstractmethod
    def load(self, start: float, end: float):
        pass

    @abstractmethod
    def delete(self, start: float, end: float):
        pass
