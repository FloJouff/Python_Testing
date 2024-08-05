import pytest
from datetime import datetime, timedelta
from flask import Flask
from server import app, competitions, clubs


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
        "numberOfPlaces": "15",
        "reservations": {},
    }
    competitions.append(test_competition)

    test_club = {"name": "TestClub", "email": "test@example.com", "points": "20"}
    clubs.append(test_club)

    yield

    # Clear after tests
    competitions.remove(test_competition)
    clubs.remove(test_club)


def test_purchase_more_than_12_places(client, setup_data):
    """When an identified user try to book more than 12 places in one time"""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "TestCompetition", "club": "TestClub", "places": "13"},
        follow_redirects=True,
    )

    assert b"You cannot book more than 12 places." in response.data
    assert response.status_code == 200


def test_cumulative_booking_more_than_12_places(client, setup_data):
    """When an identified user try to book more than 12 places in more than one time"""
    # Book 8 places first
    response = client.post(
        "/purchasePlaces",
        data={"competition": "TestCompetition", "club": "TestClub", "places": "8"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Try to book 5 more places, which should be denied
    response = client.post(
        "/purchasePlaces",
        data={"competition": "TestCompetition", "club": "TestClub", "places": "5"},
        follow_redirects=True,
    )
    assert b"You cannot book more than 12 places in total for a competition." in response.data
    assert response.status_code == 200
