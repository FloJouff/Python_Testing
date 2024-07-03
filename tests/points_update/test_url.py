import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_showSummary_url(client):
    test_email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": test_email})

    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_purchase_places_url(client):
    competition_name = "Test Competition"
    club_name = "Test Club"
    initial_competition_places = 25
    places_to_book = 5
    clubs.append({"name": club_name, "email": "test@club.com", "points": 13})
    competitions.append(
        {"name": competition_name, "date": "2020-03-27 10:00:00", "numberOfPlaces": initial_competition_places}
    )
    response = client.post(
        "/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": places_to_book}
    )

    assert response.status_code == 200

    clubs.pop()
    competitions.pop()
