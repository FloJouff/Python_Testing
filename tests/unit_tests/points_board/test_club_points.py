import json
import pytest
from server import app, competitions, clubs


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def load_data():
    # Load the original data from JSON files
    with open("./clubs.json") as f:
        clubs_data = json.load(f)["clubs"]
    with open("./competitions.json") as f:
        competitions_data = json.load(f)["competitions"]

    # Copy data to avoid mutations affecting other tests
    clubs[:] = clubs_data.copy()
    competitions[:] = competitions_data.copy()

    yield

    # Optionally, clear the data after the test if needed
    clubs.clear()
    competitions.clear()


@pytest.fixture
def clubs_data():
    with open("./clubs.json") as f:
        return json.load(f)["clubs"]


def test_club_points(client, load_data, clubs_data):
    """When an unidentified user accesses the clubs' points board, the points must display correctly"""

    # Get the points board page
    response = client.get("/pointsBoard/")
    assert response.status_code == 200

    # Decode the HTML response
    html = response.data.decode("utf-8")

    # Check each club's name and points are in the HTML
    for club in clubs_data:
        assert club["name"] in html
        assert str(club["points"]) in html
