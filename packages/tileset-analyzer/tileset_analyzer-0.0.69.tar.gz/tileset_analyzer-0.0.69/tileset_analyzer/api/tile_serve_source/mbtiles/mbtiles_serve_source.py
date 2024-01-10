from tileset_analyzer.data_source.mbtiles.sqllite_utils import create_connection
from tileset_analyzer.entities.job_param import JobParam

conn = None


def get_mbtiles_source(job_param: JobParam, z: int, x: int, y: int):
    global conn

    if conn is None:
        conn = create_connection(job_param.source)

    cur = conn.cursor()
    sql = 'select {tile_data} from {tiles} where {zoom_level} = {z} and {tile_row} = {x} and {tile_column} = {y}'.format(
            **{
                'tiles': job_param.mbtiles_tbl.tiles,
                'tile_row': job_param.mbtiles_tbl.tile_row,
                'tile_column': job_param.mbtiles_tbl.tile_column,
                'zoom_level': job_param.mbtiles_tbl.zoom_level,
                'tile_data': job_param.mbtiles_tbl.tile_data,
                'z': z,
                'x': x,
                'y': y
            })
    cur.execute(sql)
    row = cur.fetchone()

    if row:
        return row[0]
    return None
