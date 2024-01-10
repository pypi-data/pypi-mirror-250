import sys
from pathlib import Path
from typing import List
from tileset_analyzer.data_source.ds_utils import get_attr, _processed_data
from tileset_analyzer.data_source.folder_tiles.folder_utils import get_folder_size, list_files_dir
from tileset_analyzer.data_source.tile_source import TileSource
from tileset_analyzer.entities.job_param import JobParam
from tileset_analyzer.entities.layer_level_size import LayerLevelSize, TileItemSize
from tileset_analyzer.entities.level_count import LevelCount
from tileset_analyzer.entities.level_size import LevelSize
from tileset_analyzer.entities.tile_item import TileItem
from tileset_analyzer.entities.tileset_analysis_result import TilesetAnalysisResult
from tileset_analyzer.entities.tileset_info import TilesetInfo
import numpy as np
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
from tileset_analyzer.readers.vector_tile.engine import VectorTile
from tileset_analyzer.utilities.moniter import timeit
from parse import compile


class FolderTilesSource(TileSource):
    def __init__(self, job_param: JobParam):
        self.job_param = job_param
        self.tiles: List[TileItem] | None = None
        self.all_tile_sizes = None
        self.compiled_pattern = compile(job_param.folder_path_scheme)

    def count_tiles(self) -> int:
        return len(self.tiles)

    def count_tiles_by_z(self) -> List[LevelCount]:
        z_count = dict()
        for tile in self.tiles:
            if tile.z not in z_count:
                z_count[tile.z] = 0
            z_count[tile.z] += 1

        result: List[LevelCount] = []
        for z in sorted(z_count.keys()):
            result.append(LevelCount(z, z_count[z]))
        return result

    def _tiles_size_agg(self, agg_type: str) -> List[LevelSize]:
        z_size = dict()
        for tile in self.tiles:
            if tile.z not in z_size:
                z_size[tile.z] = []
            z_size[tile.z].append(len(tile.data))

        result: List[LevelSize] = []
        for z in sorted(z_size.keys()):
            if agg_type == 'SUM':
                result.append(LevelSize(z, float(np.array(z_size[z]).sum())))
            elif agg_type == 'MIN':
                result.append(LevelSize(z, float(np.array(z_size[z]).min())))
            elif agg_type == 'MAX':
                result.append(LevelSize(z, float(np.array(z_size[z]).max())))
            elif agg_type == 'AVG':
                result.append(LevelSize(z, float(np.array(z_size[z]).mean())))
            elif agg_type == '50p':
                result.append(LevelSize(z, float(np.percentile(np.array(z_size[z]), 50))))
            elif agg_type == '85p':
                result.append(LevelSize(z, float(np.percentile(np.array(z_size[z]), 85))))
            elif agg_type == '90p':
                result.append(LevelSize(z, float(np.percentile(np.array(z_size[z]), 90))))
            elif agg_type == '95p':
                result.append(LevelSize(z, float(np.percentile(np.array(z_size[z]), 95))))
            elif agg_type == '99p':
                result.append(LevelSize(z, float(np.percentile(np.array(z_size[z]), 99))))
        return result

    def tiles_size_agg_sum_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('SUM')

    def tiles_size_agg_min_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('MIN')

    def tiles_size_agg_max_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('MAX')

    def tiles_size_agg_avg_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('AVG')

    def tiles_size_agg_50p_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('50p')

    def tiles_size_agg_85p_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('85p')

    def tiles_size_agg_90p_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('90p')

    def tiles_size_agg_95p_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('95p')

    def tiles_size_agg_99p_by_z(self) -> List[LevelSize]:
        return self._tiles_size_agg('99p')

    def _get_all_tiles(self) -> List[TileItem]:
        files = list_files_dir(self.job_param.source, ['*.pbf', '*.mvt'])
        result: List[TileItem] = []
        for file, data in files:
            parsed = self.compiled_pattern.parse(file)
            result.append(TileItem(int(parsed['x']), int(parsed['y']), int(parsed['z']), data))
        return result

    def _clear_all_tiles(self):
        self.tiles = None

    def tileset_info(self) -> TilesetInfo:
        tileset_info = TilesetInfo()

        loc = str(Path(self.job_param.source).absolute())
        tileset_info.set_name(Path(self.job_param.source).absolute().name)
        tileset_info.set_size(get_folder_size(loc))
        tileset_info.set_scheme(self.job_param.scheme)
        tileset_info.set_location(loc)
        tileset_info.set_ds_type('folder')
        tileset_info.set_compression(self.job_param.compressed, self.job_param.compression_type)

        self.tiles = self._get_all_tiles()
        all_layers = get_attr(self.tiles, self.job_param.compressed, self.job_param.compression_type)
        tileset_info.set_layer_info(all_layers)
        return tileset_info

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
                    layer_sizes.get(layer_name).append(layer_size)
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

    @timeit
    def _preprocess_tile_layer_sizes(self):
        all_tile_sizes: dict[str, List[TileItemSize]] = {}
        tiles = self.tiles

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

            data = _processed_data(tile.data, self.job_param.compressed, self.job_param.compression_type)
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

    def analyze(self) -> TilesetAnalysisResult:
        result = TilesetAnalysisResult()
        result.set_tileset_info(self.tileset_info())
        result.set_count_tiles_total(self.count_tiles())
        result.set_count_tiles_by_z(self.count_tiles_by_z())
        result.set_tiles_size_agg_sum_by_z(self.tiles_size_agg_sum_by_z())
        result.set_tiles_size_agg_min_by_z(self.tiles_size_agg_min_by_z())
        result.set_tiles_size_agg_max_by_z(self.tiles_size_agg_max_by_z())
        result.set_tiles_size_agg_avg_by_z(self.tiles_size_agg_avg_by_z())
        result.set_tiles_size_agg_50p_by_z(self.tiles_size_agg_50p_by_z())
        result.set_tiles_size_agg_85p_by_z(self.tiles_size_agg_85p_by_z())
        result.set_tiles_size_agg_90p_by_z(self.tiles_size_agg_90p_by_z())
        result.set_tiles_size_agg_95p_by_z(self.tiles_size_agg_95p_by_z())
        result.set_tiles_size_agg_99p_by_z(self.tiles_size_agg_99p_by_z())

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

        self._clear_all_tiles()
        return result
