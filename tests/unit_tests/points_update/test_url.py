import pytest
from server import app, clubs, competitions
from datetime import datetime, timedelta


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_data():
    test_competition = {
        "name": "TestCompetition",
        "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "10",
    }

    competitions.extend([test_competition])

    test_club = {"name": "TestClub", "email": "test@example.com", "points": "100"}
    clubs.append(test_club)

    yield

    # Nettoyage après les tests
    competitions[:] = [comp for comp in competitions if comp["name"] != "TestCompetition"]
    clubs[:] = [club for club in clubs if club["name"] != "TestClub"]


def test_showSummary_url(client, setup_data):
    test_email = "test@example.com"
    response = client.post("/showSummary", data={"email": test_email})

    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_purchase_places_url(client, setup_data):
    places_to_book = 5
    response = client.post(
        "/purchasePlaces", data={"competition": "TestCompetition", "club": "TestClub", "places": places_to_book}
    )
    assert response.status_code == 200
