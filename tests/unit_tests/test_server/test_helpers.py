import server


def test_get_club_via_email(client, monkey_clubs):
    """Given a valid email and mocked club data,
    When calling helper_get_club_via_email,
    Then it should return the corresponding club data.
    """
    test_data = "john@simplylift.co"
    expected_result = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13",
    }

    assert server.helper_get_club_via_email(test_data) == expected_result


def test_get_club_via_invalid_email(client, monkey_clubs):
    """Given an invalid email and mocked club data,
    When calling helper_get_club_via_email,
    Then it should return None.
    """
    test_data = "wrong@email.Com"

    assert server.helper_get_club_via_email(test_data) == None


def test_get_club_via_name(client, monkeypatch, monkey_clubs):
    """Given a club name and mocked data,
    When calling helper_get_club_via_name,
    Then it should return the corresponding club data.
    """
    test_data = "Simply Lift"

    expected_result = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13",
    }

    assert server.helper_get_club_via_name(test_data) == expected_result


def test_get_club_via_invalid_name(client, monkeypatch, monkey_clubs):
    """Given an invalid club name and mocked data,
    When calling helper_get_club_via_name,
    Then it should return None.
    """
    test_data = "Not a club"

    assert server.helper_get_club_via_name(test_data) == None


def test_get_competition_via_name(client, monkeypatch, monkey_competitions):
    """Given a competition name and mocked data,
    When calling helper_get_competition_via_name,
    Then it should return the corresponding competition data.
    """
    test_data = "Spring Festival"

    expected_result = {
        "name": "Spring Festival",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    assert server.helper_get_competition_via_name(test_data) == expected_result


def test_get_competition_via_invalid_name(client, monkeypatch, monkey_competitions):
    """Given an invalid competition name and mocked data,
    When calling helper_get_competition_via_name,
    Then it should return None.
    """
    test_data = "Not a competition"

    assert server.helper_get_competition_via_name(test_data) == None
