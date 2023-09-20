import server


def test_booking_with_incorrect_club(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_competition_returns_spring_festival,
    monkey_helper_get_club_via_name_returns_none,
):
    """Given a valid competition and an invalid club,
    When accessing the /book route,
    Then it should display an error message indicating
    that the booking is invalid.
    """
    competition = "Spring Festival"
    club = "Wrong"

    response = client.get(f"/book/{competition}/{club}")

    assert (
        "book if the competition or the account is invalid. Please try again."
        in response.data.decode()
    )


def test_booking_with_incorrect_competition(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_none,
):
    """Given a invalid competition and a valid club,
    When accessing the /book route,
    Then it should display an error message indicating
    that the booking is invalid.
    """
    competition = "Wrong"
    club = "Simply Lift"

    response = client.get(f"/book/{competition}/{club}")

    assert (
        "book if the competition or the account is invalid. Please try again."
        in response.data.decode()
    )


def test_places_allowed_is_between_1_and_12(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club,
    When accessing the /book route,
    Then the input field for booking places should have
    a minimum of 1 and a maximum of 12.
    """
    competition = "Spring Festival"
    club = "Simply Lift"

    response = client.get(f"/book/{competition}/{club}")

    assert 'min="1" max="12"' in response.data.decode()


def test_places_allowed_is_between_1_and_4(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_iron_temple,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with 4 points,
    When accessing the /book route,
    Then the input field for booking places should have
    a minimum of 1 and a maximum of 4.
    """
    competition = "Spring Festival"
    club = "Iron Temple"

    response = client.get(f"/book/{competition}/{club}")

    assert 'min="1" max="4"' in response.data.decode()


def test_booking_is_impossible_for_a_club_with_zero_point(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_dummy_club,
    monkey_helper_get_competition_returns_spring_festival,
):
    """Given a valid competition and a valid club
    with 0 point,
    When accessing the /book route,
    Then it should display an error message indicating
    that the club does not have enough points to book places.
    """
    competition = "Spring Festival"
    club = "Dummy Club"

    response = client.get(f"/book/{competition}/{club}")

    assert "You do not have enough points to book places." in response.data.decode()
    assert "club@dummy.com" in response.data.decode()


def test_booking_in_past_competition_is_impossible(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_name_returns_simply_lift,
    monkey_helper_get_competition_returns_fall_classic,
):
    """Given a valid past competition and a valid club,
    When accessing the /book route,
    Then it should display an error message indicating
    that booking in a past competition is impossible.
    """
    competition = "Fall Classic"
    club = "Simply Lift"

    response = client.get(f"/book/{competition}/{club}")

    assert "Booking in a past competition is impossible." in response.data.decode()
    assert "john@simplylift.co" in response.data.decode()
