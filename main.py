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
from validation import validate_locations

do_layout()

app = FastAPI()


app.mount("/app", WSGIMiddleware(dash_app.server))


@app.get('/validate_locations')
def get_validate_locations(url: str, n: int = 10):
    obj = validate_locations(url, n)
    return JSONResponse(content=obj)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
    # dash_app.run_server(debug=True, port=8051)

# ============= EOF =============================================
