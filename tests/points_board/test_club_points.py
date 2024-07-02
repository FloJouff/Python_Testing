import json
import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_club_points(client):
    with open("./clubs.json") as f:
        clubs_data = json.load(f)["clubs"]

    response = client.get("/pointsBoard/")

    html = response.data.decode("utf-8")
    for club in clubs_data:
        assert club["name"] in html
        assert str(club["points"]) in html
