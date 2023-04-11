# ===============================================================================
# Copyright 2023 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.responses import JSONResponse

from callbacks import dash_app
from layout import do_layout
from validation import validate_locations, validate_location, validate_thing, URLError, validate_things, \
    validate_datastream, validate_sensor, validate_sensors, validate_datastreams

do_layout()

app = FastAPI()

app.mount("/app", WSGIMiddleware(dash_app.server))


@app.get("/")
async def root():
    return {"message": "Welcome to NMWDI Validation Service"}


@app.get('/validate_locations')
async def get_validate_locations(url: str, n: int = 10):
    obj = validate_locations(url, n)
    return JSONResponse(content=obj)


@app.get('/validate_things')
async def get_validate_things(url: str, n: int = 10):
    obj = validate_things(url, n)
    return JSONResponse(content=obj)


@app.get('/validate_datastreams')
async def get_validate_datastreams(url: str, n: int = 10):
    obj = validate_datastreams(url, n)
    return JSONResponse(content=obj)


@app.get('/validate_sensors')
async def get_validate_sensors(url: str, n: int = 10):
    obj = validate_sensors(url, n)
    return JSONResponse(content=obj)


@app.get('/validate_location')
async def get_validate_location(url: str):
    return response_wrapper(url, validate_location)


@app.get('/validate_thing')
async def get_validate_thing(url: str):
    return response_wrapper(url, validate_thing)


@app.get('/validate_datastream')
async def get_validate_datastream(url: str):
    return response_wrapper(url, validate_datastream)


@app.get('/validate_sensor')
async def get_validate_sensor(url: str):
    return response_wrapper(url, validate_sensor)


def response_wrapper(url, validate_func):
    try:
        obj = validate_func(url)
    except URLError:
        obj = {'error': f'invalid url: {url}'}
    return JSONResponse(content=obj)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
    # dash_app.run_server(debug=True, port=8051)

# ============= EOF =============================================
