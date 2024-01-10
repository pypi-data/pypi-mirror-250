from tileset_analyzer.api.tile_serve_source.folder_tiles.folder_serve_source import get_folder_serve_source
from tileset_analyzer.api.tile_serve_source.mbtiles.mbtiles_serve_source import get_mbtiles_source
from tileset_analyzer.entities.job_param import JobParam, TileSourceType


class TileServeSourceFactory:
    @staticmethod
    def get_tile(job_param: JobParam, z: int, x: int, y: int):
        tileset_source_type = job_param.get_source_type()
        if tileset_source_type == TileSourceType.FOLDER:
            return get_folder_serve_source(job_param, z, x, y)
        elif tileset_source_type == TileSourceType.MBTiles:
            return get_mbtiles_source(job_param, z, x, y)
        raise AssertionError("Tileset Type not supported yet")
