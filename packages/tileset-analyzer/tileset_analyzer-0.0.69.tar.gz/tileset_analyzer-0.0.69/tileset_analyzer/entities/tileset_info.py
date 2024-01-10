from typing import List

from tileset_analyzer.entities.layer_info import LayerInfo


class TilesetInfo:
    def __init__(self):
        self.name: str | None = None
        self.scheme: str | None = None
        self.size: int | None = None
        self.location: str | None = None
        self.ds_type: str | None = None
        self.layer_info_items: List[LayerInfo] | None = None
        self.compressed: bool | None = None
        self.compression_type: str | None = None

    def set_name(self, name: str):
        self.name = name

    def set_scheme(self, scheme: str):
        self.scheme = scheme

    def set_size(self, size: int):
        self.size = size

    def set_location(self, location: str):
        self.location = location

    def set_ds_type(self, ds_type: str):
        self.ds_type = ds_type

    def set_layer_info(self, layer_info_items: List[LayerInfo]):
        self.layer_info_items = layer_info_items

    def set_compression(self, compressed: bool, compression_type: str):
        self.compressed = compressed
        self.compression_type = compression_type
