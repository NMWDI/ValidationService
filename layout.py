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
import dash_bootstrap_components as dbc
import requests as requests
from dash import html, dcc
from dash.dash_table import DataTable
from dashapp import dash_app


def layout_rows():
    loading = dcc.Loading(
        id="loading-1",
        type="default",
        # fullscreen=True,
        children=html.Div(id="loading-output-1")
    )

    validate_locations_btn = dbc.Button('Validate Locations', id='validate_locations_btn')
    validate_things_btn = dbc.Button('Validate Things', id='validate_things_btn')
    validate_datastreams_btn = dbc.Button('Validate Datastreams', id='validate_datastreams_btn')
    validate_all_btn = dbc.Button('Validate All', id='validate_all_btn')
    validate_btn_grp = dbc.ButtonGroup([validate_all_btn,
                                        validate_locations_btn,
                                        validate_things_btn,
                                        validate_datastreams_btn
                                        ])
    cols = [{"name": "Name", "id": "name"},
            {"name": "@iot.id", "id": "@iot.id"},
            {"name": "ValidationError", "id": "validation_error"},
            {"name": "Instance", "id": "instance", 'presentation': 'markdown'},
            ]
    dt = DataTable(
        id='validation_results',
        style_cell={"textAlign": "left"},
        columns=cols,
        style_as_list_view=True,
        page_size=10,

        style_header={
            "font-family": "verdana",
            "font-weight": "bold",
            "fontSize": "10px",
            # "height": "50px"
        },
        style_data={"fontSize": "10px", "font-family": "verdana",
                    # 'whiteSpace': 'pre-line'
                    },
        style_table={"height": "600px", "overflowY": "auto"},
    )

    return [dbc.Row([dbc.Col([dbc.Input(id='url_to_validate',
                                       value='https://st2.newmexicowaterdata.org/FROST-Server/v1.1')]),
                    dbc.Col([dbc.Input(id='n', value=10)])
                    ]
                    ),
            dbc.Row(dbc.Col([validate_btn_grp])),
            dbc.Row(dbc.Col([dt, loading]))
            ]


def do_layout():
    dash_app.layout = dbc.Container(layout_rows())
# ============= EOF =============================================
