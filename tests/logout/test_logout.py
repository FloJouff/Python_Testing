import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_logout_url(client):
    test_email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": test_email})
    assert response.status_code == 200

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
