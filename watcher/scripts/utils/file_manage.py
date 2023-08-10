import csv
import json
import os
import shutil
from pathlib import Path


class JsonManager:
    def __init__(self, name: str = 'config.json'):
        self.name = name
        self.load()

    def load(self):
        try:
            with open(self.name, 'r', encoding="utf-8") as f:
                text = f.read()
                self.data = json.loads(text)
        except FileNotFoundError:
            self.data = {}

    def reload(self):
        self.load()

    def save(self):
        with open(self.name, 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii=False, indent=4))

    def change(self, key: str, value: any):
        self.data[key] = value
        self.save()

    def delete(self, key: str):
        del self.data[key]
        self.save()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


def get_file_dir_path(path: str) -> str:
    abspath = os.path.abspath(path)
    dirpath = os.path.dirname(abspath)
    return dirpath


def get_parents_path(path: str, level: int = 0):
    path_object = Path(path)
    return path_object.parents[level]


def substitute_path_extension(path: str, extension: str) -> str:
    path_object = Path(path)
    original_extension = path_object.suffix   # '' if directory or no extension

    if original_extension == extension:
        formatted_path = path
    else:
        formatted_path = path_object.parent.joinpath(f'{path_object.stem}.{extension}').as_posix()

    return formatted_path


def csv_writer(data_list: list, save_name: str) -> None:
    with open(save_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_list)
