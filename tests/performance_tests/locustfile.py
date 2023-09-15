from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        response = self.client.get("/")

    @task()
    def show_summary(self):
        response = self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        response = self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchase_places(self):
        response = self.client.post(
            "/purchasePlaces",
            {"competition": "Spring Festival", "club": "Simply Lift", "places": "5"},
        )

    @task
    def points(self):
        response = self.client.get("/points")

    @task
    def logout(self):
        response = self.client.get("/logout")
