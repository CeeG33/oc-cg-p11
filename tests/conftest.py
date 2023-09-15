import pytest

import server
from server import app, request


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture()
def monkey_clubs(monkeypatch):
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
    clubs = []

    monkeypatch.setattr(server, "clubs", clubs)

    return clubs


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_dummy_club(monkeypatch):
    def mockreturn():
        return {"name": "Dummy Club", "email": "club@dummy.com", "points": "0"}

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_simply_lift(monkeypatch):
    def mockreturn():
        return {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_iron_temple(monkeypatch):
    def mockreturn():
        return {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        }

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_name_returns_none(monkeypatch):
    def mockreturn():
        return None

    monkeypatch.setattr(server, "helper_get_club_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_dummy_club(monkeypatch):
    def mockreturn():
        return {"name": "Dummy Club", "email": "club@dummy.com", "points": "0"}

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_simply_lift(monkeypatch):
    def mockreturn():
        return {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_iron_temple(monkeypatch):
    def mockreturn():
        return {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        }

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_club_via_email_returns_none(monkeypatch):
    def mockreturn():
        return None

    monkeypatch.setattr(server, "helper_get_club_via_email", mockreturn)


@pytest.fixture()
def monkey_helper_get_competition_returns_spring_festival(monkeypatch):
    def mockreturn():
        return {
            "name": "Spring Festival",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "25",
        }

    monkeypatch.setattr(server, "helper_get_competition_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_competition_returns_fall_classic(monkeypatch):
    def mockreturn():
        return {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        }

    monkeypatch.setattr(server, "helper_get_competition_via_name", mockreturn)


@pytest.fixture()
def monkey_helper_get_competition_returns_none(monkeypatch):
    def mockreturn():
        return None

    monkeypatch.setattr(server, "helper_get_competition_via_name", mockreturn)


class MockRequest:
    form = {"email": "john@simplylift.co"}


@pytest.fixture()
def mock_request_valid_email():
    return MockRequest()
