from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        """Task to simulate accessing the root route ('/')
        of the application.
        """
        response = self.client.get("/")

    @task()
    def show_summary(self):
        """Task to simulate posting a request to '/show_summary'
        with a valid sample email.
        """
        response = self.client.post("/show_summary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        """Task to simulate accessing the booking page for
        the 'Spring Festival' with the 'Simply Lift' club.
        """
        response = self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchase_places(self):
        """Task to simulate purchasing 5 places for the
        'Spring Festival' with the 'Simply Lift' club.
        """
        response = self.client.post(
            "/purchase_places",
            {
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "5",
            },
        )

    @task
    def points(self):
        """Task to simulate accessing the '/points' route to view clubs points."""
        response = self.client.get("/points")

    @task
    def logout(self):
        """Task to simulate logging out by accessing the '/logout' route."""
        response = self.client.get("/logout")
