import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_points_board(client):

    response = client.get("/pointsBoard/")

    assert response.status_code == 200
    assert b"Points Board" in response.data
