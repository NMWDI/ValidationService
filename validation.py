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
import json

import requests
from dash import dcc
from jsonschema import validate, ValidationError

LOCATION_SCHEMA = None
THING_SCHEMA = None
THING_SCHEMA = {
    "$id": "https://vocab.newmexicowaterdata.org/schemas/gwl_thing",
    "title": "NMWDI Groundwater Level Thing Schema",
    "description": "",
    "version": "0.0.1",
    "type": "object",
    "required": ["name", "description", "properties"],
    "properties": {
        "name": {
            "type": "string",
            "description": "name of a Thing for groundwater levels should be `Water Well`"
        },
        "description": {
            "type": "string",
            "description": "description of this location"
        },
        "properties": {
            "type": "object",
            "description": "a flexible place to associate additional attributes with a thing",
            "required": ["welldepth", "welldepth_unit", "geologic_formation"],
            "welldepth": {
                "type": "number",
                "description": ""
            },
            "welldepth_unit": {
                "type": "string",
                "enum": [
                    "FTBGS",
                    "MBGS"
                ],
                "description": ""
            },
            "geologic_formation":
                {
                    "type": "string",
                    "description": ""
                }
        }
    }
}

DATASTREAM_SCHEMA = {
    "$id": "https://vocab.newmexicowaterdata.org/schemas/gwl_thing",
    "title": "NMWDI Groundwater Level Thing Schema",
    "description": "",
    "version": "0.0.1",
    "type": "object",
    "required": ["name", "description", "properties"],
    "properties": {
        "name": {
            "type": "string",
            "description": "name for Groundwater levels",
            "enum": ["Groundwater Levels", "Groundwater Levels(Acoustic)", "Groundwater Levels(Pressure)"]
        },
        "description": {
            "type": "string",
            "description": "description of this location"
        },
        "properties": {
            "required": ["topic"],
            "type": "object",
            "description": "a flexible place to associate additional attributes with a thing",
            "topic": {"type": "string",
                      "enum": ["Water Quantity"]}
        }
    }
}


# @app.get('/st2_validate')
# async def get_st2_validation():
#     return st2_validation(ST2)
#
# @app.get('/st_validate_location')
# async def get_st_validate_location(url: str):
#     return validate_locations(url)


def validate_locations(base_url, n=10):
    global LOCATION_SCHEMA
    if LOCATION_SCHEMA is None:
        resp = requests.get('https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/location.schema.json#')
        LOCATION_SCHEMA = resp.json()

    url = 'Locations'
    if n:
        url = f'{url}?$top={n}'

    return _validate(base_url, url, LOCATION_SCHEMA)


def validate_things(url):
    global THING_SCHEMA
    if THING_SCHEMA is None:
        resp = requests.get(
            'https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/groundwaterlevel.thing.schema.json#')
        THING_SCHEMA = resp.json()

    return _validate(url, 'Things', THING_SCHEMA)


def st_get(url, tag):
    url = f'{url}/{tag}'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(url)
        print(resp.status_code, resp.text)


def _validate(base_url, url, schema):
    failures = []
    items = st_get(base_url, url)
    for item in items['value']:
        try:
            validate(item, schema)
        except ValidationError as e:
            instance = json.dumps(e.instance, indent=2)
            failures.append({'name': item['name'], '@iot.id': item['@iot.id'],
                             'validation_error': e.message,
                             'instance':  f'''
```json
{instance}
```
'''}
                            )
    return failures


def st2_validation(url):
    global LOCATION_SCHEMA, THING_SCHEMA, DATASTREAM_SCHEMA

    if LOCATION_SCHEMA is None:
        resp = requests.get('https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/location.schema.json#')
        LOCATION_SCHEMA = resp.json()

    if THING_SCHEMA is None:
        resp = requests.get(
            'https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/groundwaterlevel.thing.schema.json#')
        THING_SCHEMA = resp.json()

    if DATASTREAM_SCHEMA is None:
        resp = requests.get(
            'https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/groundwaterlevel.datastream.schema.json#'
        )
        DATASTREAM_SCHEMA = resp.json()

    flocations = []
    fthings = []
    fdatastreams = []
    for agency in ('NMBGMR', 'EBID'):
        locations = st_get(url, f"Locations?$top=10&$filter=properties/agency eq '{agency}'&$expand=Things/Datastreams")
        for location in locations['value']:
            try:
                validate(location, LOCATION_SCHEMA)
            except ValidationError as e:
                flocations.append(e)

            for thing in location['Things']:
                try:
                    validate(thing, THING_SCHEMA)
                except ValidationError as e:
                    fthings.append(e)

                for datastream in thing['Datastreams']:
                    try:
                        validate(datastream, DATASTREAM_SCHEMA)
                    except ValidationError as e:
                        fdatastreams.append(e)

    return flocations, fthings, fdatastreams

# ============= EOF =============================================
