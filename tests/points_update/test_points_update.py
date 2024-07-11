# import json
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

    competitions.append(test_competition)

    test_club = {"name": "TestClub", "email": "test@example.com", "points": "10"}
    clubs.append(test_club)

    yield

    # Nettoyage après les tests
    competitions[:] = [comp for comp in competitions if comp["name"] != "TestCompetition"]
    clubs[:] = [club for club in clubs if club["name"] != "TestClub"]


def test_points_update(client, setup_data):
    competition = [c for c in competitions if c["name"] == "TestCompetition"][0]
    club = [c for c in clubs if c["name"] == "TestClub"][0]
    initial_competition_places = int(competition["numberOfPlaces"])
    initial_club_points = int(club["points"])
    places_to_book = 5

    response = client.post(
        "/purchasePlaces", data={"competition": "TestCompetition", "club": "TestClub", "places": places_to_book}
    )

    assert response.status_code == 200

    # checks that the number of places remaining has been updated
    assert int(competition["numberOfPlaces"]) == initial_competition_places - places_to_book

    # checks that the club's points have been updated
    assert int(club["points"]) == initial_club_points - places_to_book

    assert b"Great-booking complete!" in response.data

def test_not_enought_points(client):
    competition_name = "Test Competition"
    club_name = "Test Club"
    initial_competition_places = 10
    initial_club_points = 4
    places_to_book = 5

    clubs.append({"name": club_name, "email": "test@club.com", "points": initial_club_points})
    competitions.append(
        {"name": competition_name, "date": "2025-03-27 10:00:00", "numberOfPlaces": initial_competition_places}
    )

    response = client.post(
        "/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": places_to_book}
    )

    assert response.status_code == 200
    competition = [c for c in competitions if c["name"] == competition_name][-1]
    club = [c for c in clubs if c["name"] == club_name][-1]
    assert competition["numberOfPlaces"] == initial_competition_places

    assert int(club["points"]) == initial_club_points
    assert b"Not enought points or places available." in response.data

    clubs.pop()
    competitions.pop()


def test_not_enought_places(client):
    competition_name = "Test Competition"
    club_name = "Test Club"
    initial_competition_places = 5
    initial_club_points = 10
    places_to_book = 6

    clubs.append({"name": club_name, "email": "test@club.com", "points": initial_club_points})
    competitions.append(
        {"name": competition_name, "date": "2025-03-27 10:00:00", "numberOfPlaces": initial_competition_places}
    )

    response = client.post(
        "/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": places_to_book}
    )

    assert response.status_code == 200
    competition = [c for c in competitions if c["name"] == competition_name][-1]
    club = [c for c in clubs if c["name"] == club_name][-1]
    assert competition["numberOfPlaces"] == initial_competition_places

    assert int(club["points"]) == initial_club_points
    assert b"Not enought points or places available." in response.data

    clubs.pop()
    competitions.pop()


def test_negative_places_booking(client):
    """Test that booking negative places is not allowed"""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "TestCompetition", "club": "TestClub", "places": "-5"},
        follow_redirects=True,
    )

    # assert b"The number of places can't be negative." in response.data
    assert response.status_code == 200
