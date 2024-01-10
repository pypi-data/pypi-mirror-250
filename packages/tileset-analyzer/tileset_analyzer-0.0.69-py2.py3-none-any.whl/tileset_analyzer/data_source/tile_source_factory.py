from tileset_analyzer.data_source.folder_tiles.folder_tiles_source import FolderTilesSource
from tileset_analyzer.data_source.mbtiles.mbtiles_source import MBTilesSource
from tileset_analyzer.entities.job_param import JobParam, TileSourceType


class TilesetSourceFactory:
    @staticmethod
    def get_tileset_source(job_param: JobParam):
        tileset_source_type = job_param.get_source_type()
        if tileset_source_type == TileSourceType.FOLDER:
            return FolderTilesSource(job_param)
        elif tileset_source_type == TileSourceType.MBTiles:
            return MBTilesSource(job_param)
        raise AssertionError("Tileset Type not supported yet")
