import pytest
from server import app


class TestShowSummary:
    def setup_method(self, clubs):
        clubs = clubs
        
    def teardown_method(self):
        pass
        
    def test_show_summary_with_existing_email(self, client):
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert b"john@simplylift.co" in response.data
        
    def test_login_with_invalid_email(self, client):
        response = client.post("/showSummary", data={"email": "wrong@email.com"})
        assert b"Email not found. Please try a valid email." in response.data

class TestPurchasePlaces:
    def setup_method(self):
        competition = single_competition["name"]
        club = single_club["name"]
        # club_points = int(single_club["points"])
    
    def teardown_method(self):
        pass
        
    def test_purchase_places_with_enough_points(self, client):
        places_booked = 5
        response = client.post("/purchasePlaces", data={"places": places_booked})
        
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        
    def test_purchase_places_with_excessive_points(self, client):
        places_booked = 20
        response = client.post("/purchasePlaces", data={"places": places_booked})
        
        assert "have enough points to book this quantity. Please try again." in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        
    def test_purchase_places_with_negative_input(self, client):
        places_booked = -2
        response = client.post("/purchasePlaces", data={"places": places_booked})
        
        assert "This is not a correct value. Please try again." in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        
    def test_cannot_purchase_more_than_12_places(self, client):
        places_booked = 15
        response = client.post("/purchasePlaces", data={"places": places_booked})
        
        assert "have enough points to book this quantity. Please try again." in response.data.decode()
        
class TestBook:
    def test_places_allowed_is_between_1_and_12(self, client, single_club, single_competition):
        competition = single_competition["name"]
        club = single_club["name"]

        response = client.get(f"/book/{competition}/{club}")
        print(response.data)
        
        assert 'min="1" max="12"' in response.data.decode()
        