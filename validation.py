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
import os

import requests
from dash import dcc
from jsonschema import validate, ValidationError

LOCATION_SCHEMA = None
THING_SCHEMA = None

if os.environ.get('USE_LOCAL_SCHEMA', False):
    with open('schemas/locations.json') as fp:
        LOCATION_SCHEMA = json.load(fp)
    with open('schemas/things.json') as fp:
        THING_SCHEMA = json.load(fp)
else:
    resp = requests.get('https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/v0/locations.json#')
    LOCATION_SCHEMA = resp.json()

    resp = requests.get(
        'https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/v0/groundwaterlevel.things.json#')
    THING_SCHEMA = resp.json()

    resp = requests.get(
        'https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/v0/groundwaterlevel.datastreams.json#')
    DATASTREAM_SCHEMA = resp.json()

    resp = requests.get(
        'https://raw.githubusercontent.com/NMWDI/VocabService/main/schemas/v0/groundwaterlevel.sensors.json#')
    SENSOR_SCHEMA = resp.json()


# Locations
def validate_locations(base_url, n=10):
    return _validate_location(base_url, n)


def validate_location(base_url):
    return _validate_location(base_url)


# ===============================================================================

# Things
def validate_things(base_url, n=10):
    return _validate_thing(base_url, n)


def validate_thing(base_url):
    return _validate_thing(base_url)


# ===============================================================================

# Datastreams
def validate_datastreams(base_url, n=10):
    return _validate_datastream(base_url, n=n)


def validate_datastream(base_url):
    return _validate_datastream(base_url)


# ===============================================================================

# Sensors
def validate_sensors(base_url, n=10):
    return _validate_sensor(base_url, n=n)


def validate_sensor(base_url):
    return _validate_sensor(base_url)


# ===============================================================================
def _validate_sensor(base_url, n=0):
    params = None
    if n:
        params = {'$top': n}
    base_url = f'{base_url}/Sensors'
    return _validate(base_url, SENSOR_SCHEMA, params=params)


def _validate_location(base_url, n=0):
    params = None
    if n:
        params = {'$top': n}
    base_url = f'{base_url}/Locations'
    return _validate(base_url, LOCATION_SCHEMA, params=params)


def _validate_datastream(base_url, n=0):
    params = None
    if n:
        params = {'$top': n}
    base_url = f'{base_url}/Datastreams'
    return _validate(base_url, DATASTREAM_SCHEMA, params=params)


def _validate_thing(base_url, n=0):
    params = None
    if n:
        params = {'$top': n}

    return _validate(base_url, THING_SCHEMA, params=params)


# define a function that recursively retrieves all the items from a request
def st_get_all(url, params=None, page=0, max_pages=1, max_items=1000):
    if page >= max_pages:
        return []
    print(url, params)
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        items = resp.json()
        if 'value' in items:
            items = items['value']
        if '@iot.nextLink' in items:
            if len(max_items) <= max_items:
                items.extend(
                    st_get_all(items['@iot.nextLink'], page=page + 1, max_pages=max_pages, max_items=max_items))
        return items
    else:
        print(url)
        print(resp.status_code, resp.text)


def _validate(base_url, schema, params):
    failures = []
    items = st_get_all(base_url, params=params)
    if 'value' not in items:
        items = {'value': [items]}

    for item in items['value']:
        try:
            validate(item, schema)
        except ValidationError as e:
            instance = json.dumps(e.instance, indent=2)
            failures.append({'name': item['name'], '@iot.id': item['@iot.id'],
                             'validation_error': e.message,
                             'instance': f'''
```json
{instance}
```
'''}
                            )
    return failures

# ============= EOF =============================================
