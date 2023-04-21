from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
TEST_URL = 'https://st2.newmexicowaterdata.org/FROST-Server/v1.1'


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to NMWDI Validation Service"}


def test_validate_locations():
    response = client.get("/validate_locations", params={"url": TEST_URL})
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_validate_n_locations():
    response = client.get("/validate_locations", params={"url": TEST_URL, "n": 3})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def validate_n_things():
    response = client.get("/validate_things", params={"url": TEST_URL, "n": 3})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_validate_location():
    response = client.get("/validate_location", params={"url": f'{TEST_URL}/Locations(1)'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_validate_location_bad_url():
    response = client.get("/validate_location", params={"url": TEST_URL})
    assert response.status_code == 200
    assert response.json() == {"error": f"invalid url: {TEST_URL}"}


def test_validate_things():
    response = client.get("/validate_things", params={"url": TEST_URL})
    assert response.status_code == 200


#
def test_validate_thing():
    response = client.get("/validate_thing", params={"url": f'{TEST_URL}/Things(1)'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_validate_thing_bad_url():
    response = client.get("/validate_thing", params={"url": TEST_URL})
    assert response.status_code == 200
    assert response.json() == {"error": f"invalid url: {TEST_URL}"}


#     assert response.json() == {"msg": "Hello World"}

def test_validate_datastreams():
    response = client.get("/validate_datastreams", params={"url": TEST_URL})
    assert response.status_code == 200


def test_validate_datastream():
    response = client.get("/validate_datastream", params={"url": f'{TEST_URL}/Datastreams(1)'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_validate_datastream_bad_url():
    response = client.get("/validate_datastream", params={"url": TEST_URL})
    assert response.status_code == 200
    assert response.json() == {"error": f"invalid url: {TEST_URL}"}


def test_validate_sensors():
    response = client.get("/validate_sensors", params={"url": TEST_URL})
    assert response.status_code == 200


def test_validate_sensor():
    response = client.get("/validate_sensor", params={"url": f'{TEST_URL}/Sensors(1)'})
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    assert len(response.json()) == 1


def test_validate_sensor_bad_url():
    response = client.get("/validate_sensor", params={"url": TEST_URL})
    assert response.status_code == 200
    assert response.json() == {"error": f"invalid url: {TEST_URL}"}
