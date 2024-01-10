from main import execute
from tileset_analyzer.entities.job_param import JobParam, CompressionType, JobAction, TileScheme


def run_mbtiles_analyze(actions):
    src_path = 'data/maptiler-osm-2017-07-03-v3.6.1-us_virginia.mbtiles'
    temp_folder = 'tileset_analyzer/static/data'
    scheme = TileScheme.TMS
    actions = actions
    compressed = True
    compression_type = CompressionType.GZIP
    job_param = JobParam(
        source=src_path,
        scheme=scheme,
        temp_folder=temp_folder,
        actions=actions,
        verbose=False,
        compressed=compressed,
        compression_type=compression_type,
        mbtiles_tbl='tiles,tile_row,tile_column,zoom_level,tile_data'
    )
    execute(job_param)


def folder_tiles_analyze(actions):
    src_path = 'data/tiles/'
    temp_folder = 'tileset_analyzer/static/data'
    scheme = TileScheme.XYZ
    actions = actions
    compressed = False
    compression_type = None
    job_param = JobParam(
        source=src_path,
        scheme=scheme,
        temp_folder=temp_folder,
        actions=actions,
        verbose=False,
        compressed=compressed,
        compression_type=compression_type,
        folder_path_scheme='{z}/{x}/{y}.pbf',
        mbtiles_tbl=None
    )
    execute(job_param)


if __name__ == "__main__":
    run_mbtiles_analyze([JobAction.PROCESS, JobAction.SERVE])
    # folder_tiles_analyze([JobAction.PROCESS, JobAction.SERVE])
