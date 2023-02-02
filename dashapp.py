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
from dash import Dash

dash_app = Dash(
    'nmwdi_st_validation',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="NMWDI SensorThings Validation",
    # background_callback_manager=background_callback_manager,
)

# ============= EOF =============================================
