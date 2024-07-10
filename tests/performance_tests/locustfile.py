from locust import HttpUser, TaskSet, task, between
import json
from datetime import datetime, timedelta


class WebsiteTasks(TaskSet):
    def on_start(self):
        self.email = "test@example.com"
        self.club = {"name": "TestClub", "email": self.email, "points": "100"}
        self.future_competition = {
            "name": "FutureCompetition",
            "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "20",
        }
        self.past_competition = {
            "name": "PastCompetition",
            "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "10",
        }
        self.competitions = [self.future_competition, self.past_competition]

        # Create necessary setup for the test
        self.create_setup()

    def create_setup(self):
        self.client.post("/setup_club", json=self.club)
        self.client.post("/setup_competition", json=self.future_competition)
        self.client.post("/setup_competition", json=self.past_competition)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": self.email})

    @task
    def book_future_competition(self):
        self.client.get(f"/book/{self.future_competition['name']}/{self.club['name']}")

    @task
    def book_past_competition(self):
        self.client.get(f"/book/{self.past_competition['name']}/{self.club['name']}")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={"competition": self.future_competition["name"], "club": self.club["name"], "places": "5"},
        )

    @task
    def points_board(self):
        self.client.get("/pointsBoard/")

    @task
    def logout(self):
        self.client.get("/logout")


class WebsiteUser(HttpUser):
    tasks = [WebsiteTasks]
    wait_time = between(1, 5)
