import server


def test_show_summary_with_existing_email(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_email_returns_simply_lift,
):
    """Given an existing club's email and mocked data,
    When posting a request to /show_summary,
    Then it should display the summary page for the related club.
    """
    response = client.post("/show_summary", data={"email": "john@simplylift.co"})

    assert b"john@simplylift.co" in response.data


def test_login_with_invalid_email(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_email_returns_none,
):
    """Given an invalid club email and mocked data,
    When posting a request to /show_summary,
    Then it should display an error message indicating
    that the email is not found.
    """
    response = client.post("/show_summary", data={"email": "wrong@email.com"})

    assert b"Email not found. Please try a valid email." in response.data


def test_club_with_zero_point_cannot_access_to_booking_link(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_email_returns_dummy_club,
):
    """Given a club with zero points and mocked data,
    When posting a request to /show_summary,
    Then it should display the summary page without the 'Book Places' links.
    """
    response = client.post("/show_summary", data={"email": "club@dummy.com"})

    assert b"club@dummy.com" in response.data
    assert b"Book Places" not in response.data


def test_show_summary_with_past_competitions(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_email_returns_simply_lift,
):
    """Given an existing club email and mocked data
    including past competitions,
    When posting a request to /show_summary,
    Then it should display the past competitions
    with a 'Competition closed' message.
    """
    response = client.post("/show_summary", data={"email": "john@simplylift.co"})

    assert b"Spring Festival" in response.data
    assert b"Competition closed" in response.data


def test_cannot_access_past_competitions_booking_page(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_email_returns_simply_lift,
):
    """Given an existing club email and mocked data
    including past competitions,
    When posting a request to /show_summary,
    Then it should not display links to book places
    next to past competitions.
    """
    response = client.post("/show_summary", data={"email": "john@simplylift.co"})

    assert f'<a href="/book/Fall%20Classic/' not in response.data.decode()


def test_show_summary_with_incoming_competitions(
    client,
    monkey_clubs,
    monkey_competitions,
    monkey_helper_get_club_via_email_returns_simply_lift,
):
    """Given an existing club email and mocked data
    including future competitions,
    When posting a request to /show_summary,
    Then it should display links to book places
    for future competitions.
    """
    response = client.post("/show_summary", data={"email": "john@simplylift.co"})

    assert f'<a href="/book/Future%20Competition/' in response.data.decode()
