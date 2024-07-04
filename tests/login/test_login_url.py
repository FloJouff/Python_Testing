import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_url(client):
    test_email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": test_email})

    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_unknown_email(client):
    unknown_email = "unknown@club.com"
    response = client.post("/showSummary", data={"email": unknown_email})
    assert response.status_code == 302
    follow_response = client.get(response.headers["Location"])
    assert b"Email not found. Please try again." in follow_response.data
