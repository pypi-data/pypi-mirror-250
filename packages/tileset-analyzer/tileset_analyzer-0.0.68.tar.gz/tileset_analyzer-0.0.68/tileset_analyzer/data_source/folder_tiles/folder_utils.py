import os
from glob import glob
from typing import List


def get_folder_size(path: str) -> int:
    size = 0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size


def read_binary_file(file_path):
    with open(file_path, mode="rb") as file:
        return file.read()


def list_files_dir(directory: str, ext: List[str]):
    tiles = []
    for file_ext in ext:
        this_type_files = glob(os.path.join(directory, '**', file_ext), recursive=True)

        tiles += this_type_files
    tiles = [(tile.replace(directory, ''), read_binary_file(tile)) for tile in tiles]
    return tiles
