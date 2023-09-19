import server


def test_purchase_places_with_enough_points(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with enough points,
    When posting a request to /purchase_places
    with requested places within club's allowed point,
    Then it should complete the booking, return a 200 status code,
    and display a success message.
    """
    places_booked = 5
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert response.status_code == 200
    assert "Great, booking complete !" in response.data.decode()
    assert "Points available: 8" in response.data.decode()

def test_purchase_places_with_excessive_points(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with points,
    When posting a request to /purchase_places
    with requested places higher than clubs points,
    Then it should display an error message indicating
    that the booking quantity is not allowed.
    """
    places_booked = 20
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "You can book a maximum quantity of 12. Please try again."
        in response.data.decode()
    )
    assert "Points available: 13" in response.data.decode()

def test_purchase_places_with_negative_input(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with points,
    When posting a request to /purchase_places
    with requested places with a negative value,
    Then it should display an error message indicating
    that the input is incorrect.
    """
    places_booked = -2
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "This is not a correct value. Please try again."
        in response.data.decode()
    )
    assert "Points available: 13" in response.data.decode()

def test_purchase_places_with_zero(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with points,
    When posting a request to /purchase_places
    with requested places with zero value,
    Then it should display an error message indicating
    that the input is incorrect.
    """
    places_booked = 0
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "This is not a correct value. Please try again."
        in response.data.decode()
    )
    assert "Points available: 13" in response.data.decode()

def test_cannot_purchase_more_than_12_places(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with points,
    When posting a request to /purchase_places
    with requested places above 12,
    Then it should display an error message indicating
    that the booking quantity is not allowed.
    """
    places_booked = 13
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "You can book a maximum quantity of 12. Please try again."
        in response.data.decode()
    )

def test_cannot_purchase_in_past_competition(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_fall_classic,
):
    """Given a valid past competition and a valid club
    with points,
    When posting a request to /purchase_places,
    Then it should display an error message indicating
    that booking in a past competition is impossible.
    """
    places_booked = 5
    data = {
        "competition": "Fall Classic",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "Booking in a past competition is impossible."
        in response.data.decode()
    )

def test_club_without_point_cannot_purchase(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_dummy_club,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    without points,
    When posting a request to /purchase_places,
    Then it should display an error message indicating
    that the club does not have enough points to book places.
    """
    places_booked = 5
    data = {
        "competition": "Spring Festival",
        "club": "Dummy Club",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "You do not have enough points to book places."
        in response.data.decode()
    )

def test_purchase_places_with_invalid_club(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_none,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and an invalid club,
    When posting a request to /purchase_places,
    Then it should display an error message indicating
    that the booking is invalid.
    """
    places_booked = 5
    data = {
        "competition": "Spring Festival",
        "club": "Wrong Club",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "book if the competition or the account is invalid. Please try again."
        in response.data.decode()
    )

def test_purchase_places_with_invalid_competition(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_none,
):
    """Given a invalid competition and a valid club,
    When posting a request to /purchase_places,
    Then it should display an error message indicating
    that the booking is invalid.
    """
    places_booked = 5
    data = {
        "competition": "Wrong Competition",
        "club": "Simply Lift",
        "places": places_booked,
    }

    response = client.post("/purchase_places", data=data)

    assert (
        "book if the competition or the account is invalid. Please try again."
        in response.data.decode()
    )