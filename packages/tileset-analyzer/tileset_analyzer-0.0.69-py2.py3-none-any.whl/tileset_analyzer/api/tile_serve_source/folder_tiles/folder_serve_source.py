from tileset_analyzer.entities.job_param import JobParam
import os


def get_folder_serve_source(job_param: JobParam, z: int, x: int, y: int):
    file_relative_path = job_param.folder_path_scheme.format(z=z, x=x, y=y, prefix=f"{(x % 16):x}{(y % 16):x}")
    tile_file_path = f'{job_param.source}/{file_relative_path}'
    if not os.path.isfile(tile_file_path):
        return None
    with open(tile_file_path, mode="rb") as tile_file:
        return tile_file.read()
