from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", {"competition": "Spring Festival", "club": "She Lifts", "places": "2"})

    @task
    def pointBoard(self):
        self.client.get("/pointsBoard")

    @task
    def logout(self):
        self.client.get("/")
