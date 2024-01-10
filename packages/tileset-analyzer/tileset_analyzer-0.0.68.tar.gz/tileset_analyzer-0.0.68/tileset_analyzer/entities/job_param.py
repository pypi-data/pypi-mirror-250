from enum import Enum
from typing import List
import os
from collections import namedtuple

class JobAction(str, Enum):
    PROCESS = 'process'
    SERVE = 'serve'


class CompressionType(str, Enum):
    GZIP = 'gzip'
    None = 'none'


class TileScheme(str, Enum):
    TMS = 'TMS'
    XYZ = 'XYZ'


class TileSourceType(str, Enum):
    MBTiles = 'MBTILES'
    FOLDER = 'FOLDER'
    PMTiles = 'PMTiles'
    COMTILES = 'COMTiles'


MBTilesTBL = namedtuple('MBTilesTBL', ['tiles', 'tile_row', 'tile_column', 'zoom_level', 'tile_data'])


class JobParam:
    def __init__(self,
                 source: str = None,
                 scheme: TileScheme = None,
                 temp_folder: str = None,
                 actions: List[JobAction] = None,
                 compressed: bool = False,
                 compression_type: CompressionType | None = CompressionType.GZIP,
                 verbose: bool = False,
                 folder_path_scheme: str = None,
                 mbtiles_tbl: str | None = 'tiles,tile_row,tile_column,zoom_level,tile_data'):
        self.source = source
        self.scheme = scheme
        self.temp_folder = temp_folder
        self.actions = actions
        self.compressed = compressed
        self.compression_type = compression_type
        self.verbose = verbose
        self.folder_path_scheme = folder_path_scheme

        if mbtiles_tbl is None:
            self.mbtiles_tbl = None
        else:
            mbtiles_tbl_parts = mbtiles_tbl.split(',')
            self.mbtiles_tbl: MBTilesTBL = MBTilesTBL(mbtiles_tbl_parts[0], mbtiles_tbl_parts[1], mbtiles_tbl_parts[2], mbtiles_tbl_parts[3], mbtiles_tbl_parts[4])

        self._source_type: TileSourceType | None = None

    def get_source_type(self) -> TileSourceType:
        if self._source_type is not None:
            return self._source_type

        source_type = None
        if os.path.isdir(self.source):
            source_type = TileSourceType.FOLDER
        elif os.path.isfile(self.source) and self.source.endswith('.pmtiles'):
            source_type = TileSourceType.PMTiles
        elif os.path.isfile(self.source) and self.source.endswith('.comtiles'):
            source_type = TileSourceType.COMTILES
        elif os.path.isfile(self.source) or self.source.endswith('.mbtiles'):
            source_type = TileSourceType.MBTiles

        if source_type is None:
            raise AssertionError("Tileset Type is not valid.")

        return source_type
