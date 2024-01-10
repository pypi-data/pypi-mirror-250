import gzip
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
from tileset_analyzer.entities.job_param import CompressionType
from tileset_analyzer.entities.layer_info import LayerInfo
from tileset_analyzer.readers.vector_tile.engine import VectorTile


def _processed_data(data, compressed, compression_type):
    if compressed is False:
        return data

    if compression_type == CompressionType.GZIP:
        return gzip.decompress(data)

    raise f'UNSUPPORTED COMPRESSION TYPE {compression_type}'


def get_attr(tiles, compressed, compression_type):
    attr_info = {}

    def process_tile(tile):
        if tile.z not in attr_info:
            attr_info[tile.z] = {}

        zoom_level_info = attr_info[tile.z]

        data = _processed_data(tile.data, compressed, compression_type)
        vt = VectorTile(data)
        for layer in vt.layers:
            if layer.name not in zoom_level_info:
                zoom_level_info[layer.name] = LayerInfo(layer.name, tile.z)

            layer_info = zoom_level_info[layer.name]
            for feature in layer.features:
                layer_info.add_feature(feature.attributes.get(), feature.type)

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_tile, tiles)

    # get all layer info's
    all_layers = []
    for zoom_level in sorted(attr_info.keys()):
        layer_dict = attr_info[zoom_level]
        for layer_name in sorted(layer_dict.keys()):
            layer_item = layer_dict[layer_name]
            all_layers.append(layer_item)
    return all_layers
