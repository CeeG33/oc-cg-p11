import server


def test_server_app_works_correctly(client):
    """
    Test the server application with various requests to ensure it works correctly.

    Given:
    - A test client for making HTTP requests.

    When:
    - A GET request is made to the root ('/') route.
    - A POST request is made to '/show_summary' with a sample email.
    - A GET request is made to book a competition and club.
    - A POST request is made to '/purchase_places' to purchase 5 places.
    - A GET request is made to '/logout'.
    - A GET request is made to '/points'.

    Then:
    - The response to the root route should contain a specific message.
    - The response to '/show_summary' should contain the provided email.
    - The response to booking should display competition, club, available places, and input validation.
    - The response to purchasing places should confirm the booking and show available points.
    - The response to '/logout' should return a status code 302 (redirect).
    - The response to '/points' should display club information and available points.
    """
    response_index = client.get("/")

    assert (
        "Please enter your secretary email to continue" in response_index.data.decode()
    )

    response_show_summary = client.post(
        "/show_summary", data={"email": "john@simplylift.co"}
    )

    assert "john@simplylift.co" in response_show_summary.data.decode()

    competition = "Competition Demo"
    club = "Simply Lift"
    response_book = client.get(f"/book/{competition}/{club}")

    assert competition in response_book.data.decode()
    assert club in response_book.data.decode()
    assert "Places available: 13" in response_book.data.decode()
    assert 'min="1" max="12"' in response_book.data.decode()

    response_purchase_places = client.post(
        "/purchase_places", data={"club": club, "competition": competition, "places": 5}
    )

    assert "Great, booking complete !" in response_purchase_places.data.decode()
    assert "Points available: 8" in response_purchase_places.data.decode()

    response_logout = client.get("/logout")

    assert response_logout.status_code == 302

    response_points = client.get("/points")

    assert "Simply Lift" in response_points.data.decode()
    assert "8" in response_points.data.decode()
