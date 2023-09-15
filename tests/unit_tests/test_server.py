import pytest
import server
from server import app, helper_get_club_via_email


class TestMonkeys:
    def test_competitions_returns_monkey(self, monkey_competitions):
        expected_result = monkey_competitions

        assert server.competitions == expected_result

    def test_clubs_returns_monkey(self, monkey_clubs):
        expected_result = monkey_clubs

        assert server.clubs == expected_result


class TestShowSummary:
    def test_show_summary_with_existing_email(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_simply_lift,
    ):
        response = client.post(
            "/show_summary", data={"email": "john@simplylift.co"}
        )

        assert b"john@simplylift.co" in response.data

    def test_login_with_invalid_email(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_none,
    ):
        response = client.post(
            "/show_summary", data={"email": "wrong@email.com"}
        )

        assert b"Email not found. Please try a valid email." in response.data

    def test_club_with_zero_point_cannot_access_to_booking_link(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_dummy_club,
    ):
        response = client.post(
            "/show_summary", data={"email": "club@dummy.com"}
        )

        assert b"club@dummy.com" in response.data
        assert b"Book Places" not in response.data

    def test_show_summary_with_past_competitions(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_simply_lift,
    ):
        response = client.post(
            "/show_summary", data={"email": "john@simplylift.co"}
        )

        assert b"Spring Festival" in response.data
        assert b"Competition closed" in response.data

    def test_cannot_access_past_competitions_booking_page(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_simply_lift,
    ):
        response = client.post(
            "/show_summary", data={"email": "john@simplylift.co"}
        )

        assert f'<a href="/book/Fall%20Classic/' not in response.data.decode()

    def test_show_summary_with_incoming_competitions(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_simply_lift,
    ):
        response = client.post(
            "/show_summary", data={"email": "john@simplylift.co"}
        )

        assert (
            f'<a href="/book/Future%20Competition/' in response.data.decode()
        )


class TestPurchasePlaces:
    def test_purchase_places_with_enough_points(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        places_booked = 5
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        assert "Points available: 8" in response.data.decode()

    def test_purchase_places_with_excessive_points(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        places_booked = 20
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert (
            "You are not allowed to book this quantity. Please try again."
            in response.data.decode()
        )
        assert "Points available: 13" in response.data.decode()

    def test_purchase_places_with_negative_input(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
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
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
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
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        places_booked = 13
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert (
            "You are not allowed to book this quantity. Please try again."
            in response.data.decode()
        )

    def test_cannot_purchase_in_past_competition(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_fall_classic,
    ):
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


class TestBook:
    def test_booking_with_incorrect_club(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_competition_returns_spring_festival,
        monkey_helper_get_club_via_name_returns_none,
    ):
        competition = "Spring Festival"
        club = "Wrong"

        response = client.get(f"/book/{competition}/{club}")

        assert (
            "book if the competition or the account is invalid. Please try again."
            in response.data.decode()
        )

    def test_booking_with_incorrect_competition(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_none,
    ):
        competition = "Wrong"
        club = "Simply Lift"

        response = client.get(f"/book/{competition}/{club}")

        assert (
            "book if the competition or the account is invalid. Please try again."
            in response.data.decode()
        )

    def test_places_allowed_is_between_1_and_12(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        competition = "Spring Festival"
        club = "Simply Lift"

        response = client.get(f"/book/{competition}/{club}")

        assert 'min="1" max="12"' in response.data.decode()

    def test_places_allowed_is_between_1_and_4(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_iron_temple,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        competition = "Spring Festival"
        club = "Iron Temple"

        response = client.get(f"/book/{competition}/{club}")

        assert 'min="1" max="4"' in response.data.decode()

    def test_booking_is_impossible_for_a_club_with_zero_point(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_dummy_club,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        competition = "Spring Festival"
        club = "Dummy Club"

        response = client.get(f"/book/{competition}/{club}")

        assert (
            "You do not have enough points to book places."
            in response.data.decode()
        )
        assert "club@dummy.com" in response.data.decode()

    def test_booking_in_past_competition_is_impossible(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_fall_classic,
    ):
        competition = "Fall Classic"
        club = "Simply Lift"

        response = client.get(f"/book/{competition}/{club}")

        assert (
            "Booking in a past competition is impossible."
            in response.data.decode()
        )
        assert "john@simplylift.co" in response.data.decode()


class TestPoints:
    def test_points_page_works(self, client, monkey_clubs):
        response = client.get(f"/points")

        assert "Registered clubs' points to date" in response.data.decode()

    def test_points_page_show_existing_club_name(self, client, monkey_clubs):
        response = client.get(f"/points")

        assert "She Lifts" in response.data.decode()

    def test_points_page_show_existing_club_points(self, client, monkey_clubs):
        response = client.get(f"/points")

        assert "12" in response.data.decode()

    def test_points_page_does_not_show_invalid_club(
        self, client, monkey_clubs
    ):
        response = client.get(f"/points")

        assert "Fake Club" not in response.data.decode()

    def test_points_page_does_not_show_invalid_club_points(
        self, client, monkey_clubs
    ):
        response = client.get(f"/points")

        assert "5000" not in response.data.decode()

    def test_points_page_does_not_show_without_clubs(
        self, client, monkey_incorrect_clubs
    ):
        response = client.get(f"/points")

        assert "Page unavailable." in response.data.decode()


class TestLogout:
    def test_logout_works(self, client):
        response = client.get(f"/logout")

        response.status_code == 302
