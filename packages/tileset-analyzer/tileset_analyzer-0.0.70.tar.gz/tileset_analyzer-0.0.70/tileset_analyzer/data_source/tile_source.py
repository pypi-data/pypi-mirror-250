import abc
from typing import List

from tileset_analyzer.entities.job_param import JobParam
from tileset_analyzer.entities.layer_level_size import LayerLevelSize
from tileset_analyzer.entities.level_count import LevelCount
from tileset_analyzer.entities.level_size import LevelSize
from tileset_analyzer.entities.tileset_analysis_result import TilesetAnalysisResult
from tileset_analyzer.entities.tileset_info import TilesetInfo


class TileSource(abc.ABC):
    @abc.abstractmethod
    def __init__(self, job_param: JobParam):
        pass

    @abc.abstractmethod
    def count_tiles(self) -> int:
        pass

    @abc.abstractmethod
    def count_tiles_by_z(self) -> List[LevelCount]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_sum_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_min_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_max_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_avg_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_50p_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_85p_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_90p_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_95p_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_99p_by_z(self) -> List[LevelSize]:
        pass

    @abc.abstractmethod
    def tileset_info(self) -> TilesetInfo:
        pass

    @abc.abstractmethod
    def tiles_size_agg_sum_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_min_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_max_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_avg_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_50p_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_85p_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_90p_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_95p_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def tiles_size_agg_99p_by_z_layer(self) -> List[LayerLevelSize]:
        pass

    @abc.abstractmethod
    def analyze(self) -> TilesetAnalysisResult:
        pass
