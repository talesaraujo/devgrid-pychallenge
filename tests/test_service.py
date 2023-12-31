import pytest
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.service import app

@pytest.fixture
def client():
    return TestClient(app)

def test_post_endpoint_must_return_data_successfully(client):
    response = client.post("/weather", json={"user_id": "123"})

    assert response.status_code == 200
    assert response.json() == {
        'status': 'Now starting collecting weather info...'
    }


def test_show_weather_capture_progress(client):
    user_data = {
        "user_id": "6969",
        "request_datetime": "2023-10-10 22:17:43.794951",
        "cities": [
            {"city_id": 3439525, "temp": 13.07, "humidity": 90},
            {"city_id": 3439781, "temp": 18.75, "humidity": 84},
        ],
    }

    # Mock file
    with open(os.path.join('data', '6969.json'), 'w') as json_file:
        json.dump(user_data, json_file, indent=2)

    response = client.get("/weather/6969")
    assert response.status_code == 200
    assert response.json() == {"progress": "1.2%"} # 2 out of 167 locations

    # Remove temp mock file
    os.remove(os.path.join('data', '6969.json'))


def test_post_no_provided_user_id_must_return_empty_response(client):
    response = client.post("/weather", json={'user_id': ''})

    assert response.status_code == 422


def test_post_no_existent_user_id_must_return_not_found_error(client):
    response = client.get("/weather/6969")

    assert response.status_code == 404


def test_redirect_must_return_200(client):
    response = client.get("/")

    assert response.status_code == 200
