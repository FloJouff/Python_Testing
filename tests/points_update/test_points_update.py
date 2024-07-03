# import json
import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_points_update(client):
    competition_name = "Spring Festival"
    club_name = "Simply Lift"
    initial_competition_places = 25
    initial_club_points = 13
    places_to_book = 5

    clubs.append({"name": club_name, "email": "john@simplylift.co", "points": 13})
    competitions.append(
        {"name": competition_name, "date": "2020-03-27 10:00:00", "numberOfPlaces": initial_competition_places}
    )
    response = client.post(
        "/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": places_to_book}
    )

    assert response.status_code == 200

    # checks that the number of places remaining has been updated
    competition = [c for c in competitions if c["name"] == competition_name][0]
    assert competition["numberOfPlaces"] == initial_competition_places - places_to_book

    # checks that the club's points have been updated
    club = [c for c in clubs if c["name"] == club_name][0]
    assert int(club["points"]) == initial_club_points - places_to_book

    assert b"Great-booking complete!" in response.data

    clubs.pop()
    competitions.pop()


def test_not_enought_points(client):
    competition_name = "Test Competition"
    club_name = "Test Club"
    initial_competition_places = 25
    initial_club_points = 4
    places_to_book = 5

    clubs.append({"name": club_name, "email": "test@club.com", "points": initial_club_points})
    competitions.append(
        {"name": competition_name, "date": "2020-03-27 10:00:00", "numberOfPlaces": initial_competition_places}
    )

    response = client.post(
        "/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": places_to_book}
    )

    assert response.status_code == 200
    print(response.data)
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
        {"name": competition_name, "date": "2020-03-27 10:00:00", "numberOfPlaces": initial_competition_places}
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
