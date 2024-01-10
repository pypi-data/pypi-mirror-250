from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path
from starlette.datastructures import Headers
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, Response
from tileset_analyzer.api.tile_serve_source.tile_serve_source_repository import TileServeSourceFactory
from tileset_analyzer.entities.job_param import JobParam, TileScheme

UI_PATH = f'{Path(os.path.dirname(__file__)).parent}/static/ui'

job_param: JobParam | None = None


# https://stackoverflow.com/questions/66093397/how-to-disable-starlette-static-files-caching
class NoCacheStaticFiles(StaticFiles):
    def is_not_modified(
            self, response_headers: Headers, request_headers: Headers
    ) -> bool:
        # your own cache rules goes here...
        return False


def start_api(_job_param: JobParam):
    global job_param
    job_param = _job_param

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/api", app=NoCacheStaticFiles(directory=job_param.temp_folder), name="api")

    @app.get("/tileset/{z}/{x}/{y}.mvt")
    async def get_tile(z: int, x: int, y: int):
        data = None
        if job_param.scheme == TileScheme.TMS:
            y = (1 << z) - 1 - y
            data = TileServeSourceFactory.get_tile(job_param, z, y, x)
        elif job_param.scheme == TileScheme.XYZ:
            data = TileServeSourceFactory.get_tile(job_param, z, x, y)

        if not data:
            return Response(status_code=404)

        if job_param.compressed:
            headers = {
                "content-encoding": job_param.compression_type,
                "content-type": "application/vnd.mapbox-vector-tile",
                "Cache-Control": 'no-cache, no-store'
            }
        else:
            headers = {
                "content-type": "application/vnd.mapbox-vector-tile",
                "Cache-Control": 'no-cache, no-store'
            }
        return Response(content=data, headers=headers)

    @app.get("/")
    async def index():
        return FileResponse(f'{UI_PATH}/index.html')

    app.mount("/static", app=NoCacheStaticFiles(directory=f'{UI_PATH}/static'), name="ui")

    @app.get("/{file_name}.{file_path}")
    async def root_files(file_name: str, file_path: str):
        return FileResponse(f'{UI_PATH}/{file_name}.{file_path}')

    @app.get("/{path_name:path}")
    async def index_react_path():
        return FileResponse(f'{UI_PATH}/index.html')
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
