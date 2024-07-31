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
    future_competition = {
        "name": "FutureCompetition",
        "date": (datetime.now() + timedelta(days=30)).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "numberOfPlaces": "10",
    }
    past_competition = {
        "name": "PastCompetition",
        "date": (datetime.now() - timedelta(days=30)).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "numberOfPlaces": "10",
    }
    competitions.extend([future_competition, past_competition])

    test_club = {
        "name": "TestClub",
        "email": "test@example.com",
        "points": "100",
    }
    clubs.append(test_club)

    yield

    # Clear after tests
    competitions[:] = [comp for comp in competitions if comp["name"] not in ["FutureCompetition", "PastCompetition"]]
    clubs[:] = [club for club in clubs if club["name"] != "TestClub"]


def test_book_future_competition(client, setup_data):
    """Test if an identified user can book a incomming competition"""
    response = client.get("/book/FutureCompetition/TestClub")
    assert response.status_code == 200
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "FutureCompetition",
            "club": "TestClub",
            "places": 1,
        },
    )
    assert b"Great-booking complete!" in response.data


def test_book_past_competition(client, setup_data):
    """
    Test when an identified user book a past competition

    """
    response = client.get(
        "/book/PastCompetition/TestClub", follow_redirects=True
    )
    assert response.status_code == 200
    response = client.get("/showSummary", data={"email": "test@example.com"})
    assert response.status_code == 302


def test_book_nonexistent_competition(client, setup_data):
    """
    Test when an identified user try to book a non existent competition

    """
    response = client.get("/book/NonexistentCompetition/TestClub")
    assert response.status_code == 302  # Redirection
    response = client.get(response.location)
    assert b"Something went wrong-please try again" in response.data


def test_book_nonexistent_club(client, setup_data):
    """
    Test when an identified user from an unknown club try to book a competition

    """
    response = client.get("/book/FutureCompetition/NonexistentClub")
    assert response.status_code == 302  # Redirection
    response = client.get(response.location)
    assert b"Something went wrong-please try again" in response.data
