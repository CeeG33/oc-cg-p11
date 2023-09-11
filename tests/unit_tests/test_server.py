import pytest
import server
from server import app, competitions, clubs


class TestShowSummary:   
    def test_show_summary_with_existing_email(self, client, clubs, competitions, monkeypatch):
        monkeypatch.setattr(server, "competitions", competitions)
        monkeypatch.setattr(server, "clubs", clubs)
        
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        
        assert b"john@simplylift.co" in response.data
        
    def test_login_with_invalid_email(self, client, clubs, competitions, monkeypatch):
        monkeypatch.setattr(server, "competitions", competitions)
        monkeypatch.setattr(server, "clubs", clubs)
        response = client.post("/showSummary", data={"email": "wrong@email.com"})
        
        assert b"Email not found. Please try a valid email." in response.data
        

class TestPurchasePlaces:   
    def test_purchase_places_with_enough_points(self, client, single_club, single_competition) :
        competition = single_competition["name"]
        club = single_club["name"]
        club_points = int(single_club["points"])
        places_booked = 5

        response = client.post("/purchasePlaces", data={"club": club, "competition": competition, "places": places_booked})
        
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        
    def test_purchase_places_with_excessive_points(self, client, single_club, single_competition) :
        competition = single_competition["name"]
        club = single_club["name"]
        club_points = int(single_club["points"])
        places_booked = 20

        response = client.post("/purchasePlaces", data={"club": club, "competition": competition, "places": places_booked})
        
        assert "have enough points to book this quantity. Please try again." in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        
    def test_purchase_places_with_negative_input(self, client, single_club, single_competition) :
        competition = single_competition["name"]
        club = single_club["name"]
        club_points = int(single_club["points"])
        places_booked = -2

        response = client.post("/purchasePlaces", data={"club": club, "competition": competition, "places": places_booked})
        
        assert "This is not a correct value. Please try again." in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        