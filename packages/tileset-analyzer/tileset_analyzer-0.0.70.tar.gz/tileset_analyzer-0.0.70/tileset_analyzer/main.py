from tileset_analyzer.api.main_api import start_api
from tileset_analyzer.data_source.tile_source_factory import TilesetSourceFactory
from tileset_analyzer.entities.job_param import JobParam, CompressionType, TileScheme, JobAction
from tileset_analyzer.utilities.moniter import timeit
from tileset_analyzer.utils.json_utils import write_json_file
import sys
import os
import argparse


def execute(job_param: JobParam):
    print('started...')
    print('src_path:', job_param.source)
    print('scheme:', job_param.scheme)
    print('compressed:', job_param.compressed)
    print('compression_type:', job_param.compression_type)
    print('temp_folder:', job_param.temp_folder)
    print('actions', job_param.actions)
    print('folder_path_scheme', job_param.folder_path_scheme)
    print('mbtiles_tbl', job_param.mbtiles_tbl)
    print('verbose', job_param.verbose)

    if 'process' in job_param.actions:
        process_job(job_param)

    if 'serve' in job_param.actions:
        print('Web UI started')
        start_api(job_param)
        print('Web UI stopped')

    print('completed')


@timeit
def process_job(job_param: JobParam):
    print('processing started')
    data_source = TilesetSourceFactory.get_tileset_source(job_param)
    result = data_source.analyze()
    output_json = os.path.join(job_param.temp_folder, 'analysis_result.json')
    write_json_file(result.get_json(), output_json)
    print('processing completed')


def get_arg(param):
    source_index = sys.argv.index(param)
    val = sys.argv[source_index + 1]
    return val


def cli():
    parser = argparse.ArgumentParser(prog='tileset_analyzer')
    parser.add_argument('--source', help='source', required=True)
    parser.add_argument('--scheme', help='scheme', default=TileScheme.XYZ)
    parser.add_argument('--compressed', help='compressed', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--compression_type', help='compression_type', default=CompressionType.GZIP)
    parser.add_argument('--temp_folder', help='temp_folder', required=True)
    parser.add_argument('--actions', help='actions', default=[JobAction.PROCESS, JobAction.SERVE])
    parser.add_argument("--verbose", help="increase output verbosity", action="store_false")
    parser.add_argument('--folder_path_scheme', help='folder path scheme', default=None)
    parser.add_argument('--mbtiles_tbl', help='mbtiles tbl params', default='tiles,tile_row,tile_column,zoom_level,tile_data')

    args = parser.parse_args()
    actions = args.actions.split(',')

    job_param = JobParam(
        source=args.source,
        scheme=args.scheme,
        temp_folder=args.temp_folder,
        actions=actions,
        verbose=args.verbose,
        compressed=args.compressed,
        compression_type=args.compression_type,
        folder_path_scheme=args.folder_path_scheme,
        mbtiles_tbl=args.mbtiles_tbl)
    execute(job_param)


'''
if __name__ == "__main__":
   cli()
'''