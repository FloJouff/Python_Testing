# UTF-8
import pytest
from datetime import datetime, timedelta
from server import app, competitions, clubs


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_data():
    future_competition = {
        "name": "FutureCompetition",
        "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "10",
    }
    past_competition = {
        "name": "PastCompetition",
        "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "10",
    }
    competitions.extend([future_competition, past_competition])

    test_club = {"name": "TestClub", "email": "test@example.com", "points": "100"}
    clubs.append(test_club)

    yield

    # Nettoyage après les tests
    competitions[:] = [comp for comp in competitions if comp["name"] not in ["FutureCompetition", "PastCompetition"]]
    clubs[:] = [club for club in clubs if club["name"] != "TestClub"]


def test_book_future_competition(client, setup_data):
    response = client.get("/book/FutureCompetition/TestClub")
    assert response.status_code == 200
    assert b"How many places?" in response.data


def test_book_past_competition(client, setup_data):
    response = client.get(
        "/book/PastCompetition/TestClub", follow_redirects=True
    )
    print(response.data)
    assert response.status_code == 200
    assert b"You can t book past competition" in response.data


def test_book_nonexistent_competition(client, setup_data):
    response = client.get("/book/NonexistentCompetition/TestClub")
    assert response.status_code == 302  # Redirection
    response = client.get(response.location)
    assert b"Something went wrong-please try again" in response.data


def test_book_nonexistent_club(client, setup_data):
    response = client.get("/book/FutureCompetition/NonexistentClub")
    assert response.status_code == 302  # Redirection
    response = client.get(response.location)
    assert b"Something went wrong-please try again" in response.data


def test_purchase_places(client, setup_data):
    competition_name = "FutureCompetition"
    club_name = "TestClub"
    initial_competition_places = 10
    places_to_book = 5

    response = client.post(
        "/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": places_to_book}
    )

    assert response.status_code == 200
    competition = next(c for c in competitions if c["name"] == competition_name)
    club = next(c for c in clubs if c["name"] == club_name)
    assert competition["numberOfPlaces"] == initial_competition_places - places_to_book
    assert int(club["points"]) == 100 - places_to_book
    assert b"Great-booking complete!" in response.data
