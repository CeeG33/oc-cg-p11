import pytest
import server
from server import app

class TestMonkeys:
    def test_competitions_returns_monkey(self, monkey_competitions):
        expected_result = [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13"
            }
        ]

        assert server.competitions == expected_result
        
    def test_clubs_returns_monkey(self, monkey_clubs):
        expected_result = [
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

        assert server.clubs == expected_result

class TestShowSummary:
    def test_show_summary_with_existing_email(self, client, monkey_clubs, monkey_competitions):
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        
        assert b"john@simplylift.co" in response.data
        
    def test_login_with_invalid_email(self, client, monkey_clubs, monkey_competitions):
        response = client.post("/showSummary", data={"email": "wrong@email.com"})
        
        assert b"Email not found. Please try a valid email." in response.data
        
    def test_club_with_zero_point_cannot_access_to_booking_link(self, client, monkey_clubs, monkey_competitions):
        response = client.post("/showSummary", data={"email": "club@dummy.com"})
        
        assert b"club@dummy.com" in response.data
        assert b"Book Places" not in response.data

class TestPurchasePlaces:
    def test_purchase_places_with_enough_points(self, client, monkey_clubs, monkey_competitions):      
        places_booked = 5
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked
        }
        
        response = client.post("/purchasePlaces", data=data)
        
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        assert "Points available: 8" in response.data.decode()
        
    def test_purchase_places_with_excessive_points(self, client, monkey_clubs, monkey_competitions):
        places_booked = 20
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked
        }
        
        response = client.post("/purchasePlaces", data=data)

        assert "You are not allowed to book this quantity. Please try again." in response.data.decode()
        assert "Points available: 13" in response.data.decode()
        
    def test_purchase_places_with_negative_input(self, client, monkey_clubs, monkey_competitions):
        places_booked = -2
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked
        }
        
        response = client.post("/purchasePlaces", data=data)
        
        assert "This is not a correct value. Please try again." in response.data.decode()
        assert "Points available: 13" in response.data.decode()
        
    def test_purchase_places_with_zero(self, client, monkey_clubs, monkey_competitions):
        places_booked = 0
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked
        }
        
        response = client.post("/purchasePlaces", data=data)
        
        assert "This is not a correct value. Please try again." in response.data.decode()
        assert "Points available: 13" in response.data.decode()
        
    def test_cannot_purchase_more_than_12_places(self, client, monkey_clubs, monkey_competitions):
        places_booked = 13
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked
        }
        
        response = client.post("/purchasePlaces", data=data)
        
        assert "You are not allowed to book this quantity. Please try again." in response.data.decode()
        
class TestBook:
    def test_places_allowed_is_between_1_and_12(self, client, monkey_clubs, monkey_competitions):
        competition = "Spring Festival"
        club = "Simply Lift"

        response = client.get(f"/book/{competition}/{club}")
        
        assert 'min="1" max="12"' in response.data.decode()
        
    def test_places_allowed_is_between_1_and_4(self, client, monkey_clubs, monkey_competitions):
        competition = "Spring Festival"
        club = "Iron Temple"

        response = client.get(f"/book/{competition}/{club}")
        
        assert 'min="1" max="4"' in response.data.decode()
    
    def test_booking_is_impossible_for_a_club_with_zero_point(self, client, monkey_clubs, monkey_competitions):
        competition = "Spring Festival"
        club = "Dummy Club"

        response = client.get(f"/book/{competition}/{club}")

        assert "You do not have enough points to book places." in response.data.decode()