import base64
from typing import List
import numpy as np
from tileset_analyzer.data_source.ds_utils import get_attr
from tileset_analyzer.data_source.mbtiles.sqllite_utils import create_connection
from tileset_analyzer.data_source.tile_source import TileSource
from tileset_analyzer.entities.job_param import JobParam, CompressionType
from tileset_analyzer.entities.layer_level_size import LayerLevelSize, TileItemSize
from tileset_analyzer.entities.level_size import LevelSize
from tileset_analyzer.entities.tile_item import TileItem
from tileset_analyzer.entities.tileset_analysis_result import LevelCount, TilesetAnalysisResult
from tileset_analyzer.data_source.mbtiles.sql_queries import SQL_COUNT_TILES, SQL_COUNT_TILES_BY_Z, \
    SQL_SUM_TILE_SIZES_BY_Z, SQL_MIN_TILE_SIZES_BY_Z, SQL_MAX_TILE_SIZES_BY_Z, SQL_AVG_TILE_SIZES_BY_Z, \
    SQL_LIST_TILE_SIZES_BY_Z, SQL_ALL_TILES
import pandas as pd
from tileset_analyzer.entities.tileset_info import TilesetInfo
import os
from pathlib import Path
from tileset_analyzer.readers.vector_tile.engine import VectorTile
import gzip
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
import sys

from tileset_analyzer.utilities.moniter import timeit


class MBTilesSource(TileSource):
    def __init__(self, job_param: JobParam):
        self.job_param = job_param
        self.conn = create_connection(job_param.source)
        self.tiles_size_z_df = None
        self.all_tile_sizes = None

    def count_tiles(self) -> int:
        cur = self.conn.cursor()
        sql = SQL_COUNT_TILES.format(
            **{
                'tiles': self.job_param.mbtiles_tbl.tiles,
                'tile_row': self.job_param.mbtiles_tbl.tile_row,
                'tile_column': self.job_param.mbtiles_tbl.tile_column,
                'zoom_level': self.job_param.mbtiles_tbl.zoom_level,
                'tile_data': self.job_param.mbtiles_tbl.tile_data
            })
        cur.execute(sql)
        count = cur.fetchone()[0]
        return count

    def count_tiles_by_z(self) -> List[LevelCount]:
        cur = self.conn.cursor()
        sql = SQL_COUNT_TILES_BY_Z.format(
            **{
                'tiles': self.job_param.mbtiles_tbl.tiles,
                'tile_row': self.job_param.mbtiles_tbl.tile_row,
                'tile_column': self.job_param.mbtiles_tbl.tile_column,
                'zoom_level': self.job_param.mbtiles_tbl.zoom_level,
                'tile_data': self.job_param.mbtiles_tbl.tile_data
            })
        cur.execute(sql)
        rows = cur.fetchall()
        result: List[LevelCount] = []
        for row in rows:
            result.append(LevelCount(row[0], row[1]))
        return result

    def _get_agg_tile_size_z(self, agg_type: str) -> List[LevelSize]:
        if agg_type == 'SUM':
            sql = SQL_SUM_TILE_SIZES_BY_Z
        elif agg_type == 'MIN':
            sql = SQL_MIN_TILE_SIZES_BY_Z
        elif agg_type == 'MAX':
            sql = SQL_MAX_TILE_SIZES_BY_Z
        elif agg_type == 'AVG':
            sql = SQL_AVG_TILE_SIZES_BY_Z
        else:
            raise 'UNKNOWN AGG TYPE'

        sql = sql.format(
            **{
                'tiles': self.job_param.mbtiles_tbl.tiles,
                'tile_row': self.job_param.mbtiles_tbl.tile_row,
                'tile_column': self.job_param.mbtiles_tbl.tile_column,
                'zoom_level': self.job_param.mbtiles_tbl.zoom_level,
                'tile_data': self.job_param.mbtiles_tbl.tile_data
            })
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        result: List[LevelSize] = []
        for row in rows:
            result.append(LevelSize(row[0], row[1]))
        return result

    def _get_all_tiles(self) -> List[TileItem]:
        cur = self.conn.cursor()
        sql = SQL_ALL_TILES.format(
            **{
                'tiles': self.job_param.mbtiles_tbl.tiles,
                'tile_row': self.job_param.mbtiles_tbl.tile_row,
                'tile_column': self.job_param.mbtiles_tbl.tile_column,
                'zoom_level': self.job_param.mbtiles_tbl.zoom_level,
                'tile_data': self.job_param.mbtiles_tbl.tile_data
            })
        cur.execute(sql)
        rows = cur.fetchall()
        result: List[TileItem] = []
        for row in rows:
            result.append(TileItem(row[0], row[1], row[2], row[3]))
        return result

    def _set_tilesize_z_dataframe(self):
        sql = SQL_LIST_TILE_SIZES_BY_Z.format(
            **{
                'tiles': self.job_param.mbtiles_tbl.tiles,
                'tile_row': self.job_param.mbtiles_tbl.tile_row,
                'tile_column': self.job_param.mbtiles_tbl.tile_column,
                'zoom_level': self.job_param.mbtiles_tbl.zoom_level,
                'tile_data': self.job_param.mbtiles_tbl.tile_data
            })
        query = sql
        cur = self.conn.cursor()
        self.tiles_size_z_df = pd.read_sql(query, self.conn)
        cur.close()

    def _clear_tilesize_z_dataframe(self):
        self.tiles_size_z_df = None

    def _get_agg_tile_size_percentiles_z(self, percentile_type: str) -> List[LevelSize]:
        if percentile_type == '50p':
            quantile = 0.5
        elif percentile_type == '85p':
            quantile = 0.85
        elif percentile_type == '90p':
            quantile = 0.9
        elif percentile_type == '95p':
            quantile = 0.95
        elif percentile_type == '99p':
            quantile = 0.99
        else:
            raise 'UNKNOWN PERCENTILE TYPE'

        result_df = self.tiles_size_z_df.groupby('zoom_level').quantile(quantile)
        result: List[LevelSize] = []
        for row in result_df.itertuples():
            result.append(LevelSize(row[0], row[1]))
        return result

    def tiles_size_agg_min_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('MIN')

    def tiles_size_agg_max_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('MAX')

    def tiles_size_agg_avg_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('AVG')

    def tiles_size_agg_sum_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('SUM')

    def tiles_size_agg_50p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('50p')

    def tiles_size_agg_85p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('85p')

    def tiles_size_agg_90p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('90p')

    def tiles_size_agg_95p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('95p')

    def tiles_size_agg_99p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('99p')

    def _processed_data(self, data):
        if self.job_param.compressed is False:
            return base64.encodestring(data)

        if self.job_param.compression_type == CompressionType.GZIP:
            return gzip.decompress(data)

        raise f'UNSUPPORTED COMPRESSION TYPE {self.job_param.compression_type}'

    @timeit
    def tileset_info(self) -> TilesetInfo:
        tileset_info = TilesetInfo()
        tileset_info.set_name((self.job_param.source.split('/')[-1]).split('.')[0])
        tileset_info.set_size(os.stat(self.job_param.source).st_size)
        tileset_info.set_scheme(self.job_param.scheme)
        tileset_info.set_location(str(Path(self.job_param.source).parent.absolute()))
        tileset_info.set_ds_type('mbtiles')
        tileset_info.set_compression(self.job_param.compressed, self.job_param.compression_type)

        tiles = self._get_all_tiles()
        all_layers = get_attr(tiles, self.job_param.compressed, self.job_param.compression_type)
        tileset_info.set_layer_info(all_layers)
        return tileset_info

    @timeit
    def _preprocess_tile_layer_sizes(self):
        all_tile_sizes: dict[str, List[TileItemSize]] = {}
        tiles = self._get_all_tiles()

        def normalize_tile_sizes(total: int, layers: dict[str, int]) -> dict[str, int]:
            final = {}
            layer_sum = sum([layer_size for layer_size in layers.values()])
            for layer_name, layer_size in layers.items():
                final[layer_name] = round((layer_size / layer_sum) * total)
            return final

        def process_tile(tile):
            if tile.z not in all_tile_sizes:
                all_tile_sizes[tile.z] = []

            level_tile_sizes = all_tile_sizes[tile.z]

            data = self._processed_data(tile.data)
            size = sys.getsizeof(tile.data)
            vt = VectorTile(data)
            tile_all_layers_size = {}
            for layer in vt.layers:
                tile_layer_size = 0
                for feature in layer.features:
                    attr = feature.attributes.get()
                    geom = feature.get_geometry()
                    tile_layer_size += (sys.getsizeof(attr) + sys.getsizeof(geom))
                tile_all_layers_size[layer.name] = tile_layer_size
            tile_all_layers_size = normalize_tile_sizes(size, tile_all_layers_size)
            level_tile_sizes.append(TileItemSize(tile.x, tile.y, tile.z, size, tile_all_layers_size))

        with Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(process_tile, tiles)

        self.all_tile_sizes = all_tile_sizes

    def _preprocess_tile_layer_sizes_clear(self):
        self.all_tile_sizes = None

    @timeit
    def tiles_size_agg_sum_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = sum([tile.size for tile in tiles])
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = 0
                    layer_sizes[layer_name] += layer_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_min_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_size == 0:
                        continue
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.min(arr))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_max_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.max(arr))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_avg_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.average(arr))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_50p_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.percentile(arr, 50))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_85p_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.percentile(arr, 85))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_90p_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.percentile(arr, 90))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_95p_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.percentile(arr, 95))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    @timeit
    def tiles_size_agg_99p_by_z_layer(self) -> List[LayerLevelSize]:
        result: List[LayerLevelSize] = []
        for z in sorted(self.all_tile_sizes.keys()):
            tiles = self.all_tile_sizes[z]
            total = 0
            layer_sizes = {}
            for item in tiles:
                for layer_name, layer_size in item.layers.items():
                    if layer_name not in layer_sizes:
                        layer_sizes[layer_name] = []
                    layer_sizes[layer_name].append(layer_size)
            for layer_name in layer_sizes.keys():
                arr = np.array(layer_sizes[layer_name])
                tile_size = int(np.percentile(arr, 99))
                layer_sizes[layer_name] = tile_size
                total += tile_size
            result.append(LayerLevelSize(z, total, layer_sizes))

        return result

    def analyze(self) -> TilesetAnalysisResult:
        result = TilesetAnalysisResult()
        result.set_count_tiles_total(self.count_tiles())
        result.set_count_tiles_by_z(self.count_tiles_by_z())
        result.set_tiles_size_agg_sum_by_z(self.tiles_size_agg_sum_by_z())
        result.set_tiles_size_agg_min_by_z(self.tiles_size_agg_min_by_z())
        result.set_tiles_size_agg_max_by_z(self.tiles_size_agg_max_by_z())
        result.set_tiles_size_agg_avg_by_z(self.tiles_size_agg_avg_by_z())

        self._set_tilesize_z_dataframe()
        result.set_tiles_size_agg_50p_by_z(self.tiles_size_agg_50p_by_z())
        result.set_tiles_size_agg_85p_by_z(self.tiles_size_agg_85p_by_z())
        result.set_tiles_size_agg_90p_by_z(self.tiles_size_agg_90p_by_z())
        result.set_tiles_size_agg_95p_by_z(self.tiles_size_agg_95p_by_z())
        result.set_tiles_size_agg_99p_by_z(self.tiles_size_agg_99p_by_z())
        self._clear_tilesize_z_dataframe()

        result.set_tileset_info(self.tileset_info())

        self._preprocess_tile_layer_sizes()
        result.set_tiles_size_agg_sum_by_z_layer(self.tiles_size_agg_sum_by_z_layer())
        result.set_tiles_size_agg_min_by_z_layer(self.tiles_size_agg_min_by_z_layer())
        result.set_tiles_size_agg_max_by_z_layer(self.tiles_size_agg_max_by_z_layer())
        result.set_tiles_size_agg_avg_by_z_layer(self.tiles_size_agg_avg_by_z_layer())
        result.set_tiles_size_agg_50p_by_z_layer(self.tiles_size_agg_50p_by_z_layer())
        result.set_tiles_size_agg_85p_by_z_layer(self.tiles_size_agg_85p_by_z_layer())
        result.set_tiles_size_agg_90p_by_z_layer(self.tiles_size_agg_90p_by_z_layer())
        result.set_tiles_size_agg_95p_by_z_layer(self.tiles_size_agg_95p_by_z_layer())
        result.set_tiles_size_agg_99p_by_z_layer(self.tiles_size_agg_99p_by_z_layer())
        self._preprocess_tile_layer_sizes_clear()

        return result
