import pytest

import server
from server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture()
def monkey_clubs(monkeypatch):
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {   "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        },
        {
            "name": "Dummy Club",
            "email": "club@dummy.com",
            "points": "0"
        }
    ]
    
    monkeypatch.setattr(server, "clubs", clubs)
    
    return clubs
    
@pytest.fixture()
def monkey_competitions(monkeypatch):
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Future Competition",
            "date": "2030-10-22 13:30:00",
            "numberOfPlaces": "15"
        }
    ]
    
    monkeypatch.setattr(server, "competitions", competitions)
    
    return competitions

@pytest.fixture()
def monkey_incorrect_clubs(monkeypatch):
    clubs = []
    
    monkeypatch.setattr(server, "clubs", clubs)
    
    return clubs