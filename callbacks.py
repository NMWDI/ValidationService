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
from dash import Output, Input, State, ctx

from dashapp import dash_app
from validation import validate_locations, validate_things, validate_datastreams


@dash_app.callback([Output('validation_results', 'data'),
                    Output("loading-output-1", "children")],
                   [Input('validate_locations_btn', 'n_clicks'),
                    Input('validate_things_btn', 'n_clicks'),
                    Input('validate_datastreams_btn', 'n_clicks'),
                    Input('validate_all_btn', 'n_clicks'),
                    State('url_to_validate', 'value'),
                    State("n", "value")
                    ],
                   prevent_initial_call=True
                   )
def handle_validate(vlocations, vthings, vds, vall, url, n):
    validation_results = []
    func = None
    if ctx.triggered_id == 'validate_all_btn':
        pass
    elif ctx.triggered_id == 'validate_locations_btn':
        func = validate_locations
    elif ctx.triggered_id == 'validate_things_btn':
        func = validate_things
    elif ctx.triggered_id == 'validate_datastreams_btn':
        func = validate_datastreams

    if func:
        validation_results = func(url, n)

    return validation_results, ''
# ============= EOF =============================================
