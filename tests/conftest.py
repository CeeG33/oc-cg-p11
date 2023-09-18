import pytest

import server
from server import app


@pytest.fixture
def client():
    """Create and configure a test client for the Flask app."""
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture()
def monkey_clubs(monkeypatch):
    """Fixture to provide mocked club data for testing.

    Returns:
        list[dict]: A list of dictionaries representing club data.
    """
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        {"name": "Dummy Club", "email": "club@dummy.com", "points": "0"},
    ]

    monkeypatch.setattr(server, "clubs", clubs)

    return clubs


@pytest.fixture()
def monkey_competitions(monkeypatch):
    """Fixture to provide mocked competition data for testing.

    Returns:
        list[dict]: A list of dictionaries representing competition data.
    """
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
        {
            "name": "Future Competition",
            "date": "2030-10-22 13:30:00",
            "numberOfPlaces": "15",
        },
    ]

    monkeypatch.setattr(server, "competitions", competitions)

    return competitions


@pytest.fixture()
def monkey_incorrect_clubs(monkeypatch):
    """Fixture to provide an empty list of clubs for testing
    when clubs do not exist.

    Returns:
        list[dict]: An empty list of dictionaries representing club data.
    """
    clubs = []

    monkeypatch.setattr(server, "clubs", clubs)

    return clubs


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_dummy_club(monkeypatch):
    """Fixture to mock the helper_get_club_via_name function returning
    dummy club data.
    """

    def mockreturn(*args, **kwargs):
        return {"name": "Dummy Club", "email": "club@dummy.com", "points": "0"}

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_simply_lift(monkeypatch):
    """Fixture to mock the helper_get_club_via_name function returning
    Simply Lift club data.
    """

    def mockreturn(*args, **kwargs):
        return {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_iron_temple(monkeypatch):
    """Fixture to mock the helper_get_club_via_name function returning
    Iron Temple club data.
    """

    def mockreturn(*args, **kwargs):
        return {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        }

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_none(monkeypatch):
    """Fixture to mock the scenario when the club is not found."""

    def mockreturn(*args, **kwargs):
        return None

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_dummy_club(monkeypatch):
    """Fixture to mock the helper_get_club_via_email function returning
    dummy club data.
    """

    def mockreturn(*args, **kwargs):
        return {"name": "Dummy Club", "email": "club@dummy.com", "points": "0"}

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_simply_lift(monkeypatch):
    """Fixture to mock the helper_get_club_via_email function returning
    Simply Lift club data.
    """

    def mockreturn(*args, **kwargs):
        return {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_iron_temple(monkeypatch):
    """Fixture to mock the helper_get_club_via_email function returning
    Iron Temple club data.
    """

    def mockreturn(*args, **kwargs):
        return {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        }

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_none(monkeypatch):
    """Fixture to mock the scenario when the club is not found."""

    def mockreturn(*args, **kwargs):
        return None

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_competition_returns_spring_festival(monkeypatch):
    """Fixture to mock the helper_get_competition_via_name function
    returning Spring Festival competition data.
    """

    def mockreturn(*args, **kwargs):
        return {
            "name": "Spring Festival",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "25",
        }

    monkeypatch.setattr(server, "helper_get_competition_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_competition_returns_fall_classic(monkeypatch):
    """Fixture to mock the helper_get_competition_via_name function
    returning Fall Classic competition data.
    """

    def mockreturn(*args, **kwargs):
        return {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        }

    monkeypatch.setattr(server, "helper_get_competition_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_competition_returns_none(monkeypatch):
    """Fixture to mock the scenario when the competition is not found."""

    def mockreturn(*args, **kwargs):
        return None

    monkeypatch.setattr(server, "helper_get_competition_via_name", mockreturn)
