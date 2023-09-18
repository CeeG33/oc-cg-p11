import server


class TestMonkeys:
    def test_competitions_returns_monkey(self, monkey_competitions):
        """Given competitions data is mocked,
        When accessing server.py competitions variable,
        Then it should return the mocked competitions data.
        """
        expected_result = monkey_competitions

        assert server.competitions == expected_result

    def test_clubs_returns_monkey(self, monkey_clubs):
        """Given clubs data is mocked,
        When accessing server.py clubs variable,
        Then it should return the mocked clubs data.
        """
        expected_result = monkey_clubs

        assert server.clubs == expected_result


class TestHelpers:
    def test_get_club_via_email(self, client, monkey_clubs):
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

    def test_get_club_via_invalid_email(self, client, monkey_clubs):
        """Given an invalid email and mocked club data,
        When calling helper_get_club_via_email,
        Then it should return None.
        """
        test_data = "wrong@email.Com"

        assert server.helper_get_club_via_email(test_data) == None

    def test_get_club_via_name(self, client, monkeypatch, monkey_clubs):
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

    def test_get_club_via_invalid_name(
        self, client, monkeypatch, monkey_clubs
    ):
        """Given an invalid club name and mocked data,
        When calling helper_get_club_via_name,
        Then it should return None.
        """
        test_data = "Not a club"

        assert server.helper_get_club_via_name(test_data) == None

    def test_get_competition_via_name(
        self, client, monkeypatch, monkey_competitions
    ):
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

        assert (
            server.helper_get_competition_via_name(test_data)
            == expected_result
        )

    def test_get_competition_via_invalid_name(
        self, client, monkeypatch, monkey_competitions
    ):
        """Given an invalid competition name and mocked data,
        When calling helper_get_competition_via_name,
        Then it should return None.
        """
        test_data = "Not a competition"

        assert server.helper_get_competition_via_name(test_data) == None


class TestShowSummary:
    def test_show_summary_with_existing_email(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_email_returns_simply_lift,
    ):
        """Given an existing club's email and mocked data,
        When posting a request to /show_summary,
        Then it should display the summary page for the related club.
        """
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
        """Given an invalid club email and mocked data,
        When posting a request to /show_summary,
        Then it should display an error message indicating
        that the email is not found.
        """
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
        """Given a club with zero points and mocked data,
        When posting a request to /show_summary,
        Then it should display the summary page without the 'Book Places' links.
        """
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
        """Given an existing club email and mocked data
        including past competitions,
        When posting a request to /show_summary,
        Then it should display the past competitions
        with a 'Competition closed' message.
        """
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
        """Given an existing club email and mocked data
        including past competitions,
        When posting a request to /show_summary,
        Then it should not display links to book places
        next to past competitions.
        """
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
        """Given an existing club email and mocked data
        including future competitions,
        When posting a request to /show_summary,
        Then it should display links to book places
        for future competitions.
        """
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
        """Given a valid competition and a valid club
        with enough points,
        When posting a request to /purchase_places
        with requested places within club's allowed point,
        Then it should complete the booking, return a 200 status code,
        and display a success message.
        """
        places_booked = 5
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert response.status_code == 200
        assert "Great, booking complete !" in response.data.decode()
        assert "Points available: 8" in response.data.decode()

    def test_purchase_places_with_excessive_points(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        """Given a valid competition and a valid club
        with points,
        When posting a request to /purchase_places
        with requested places higher than clubs points,
        Then it should display an error message indicating
        that the booking quantity is not allowed.
        """
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
        """Given a valid competition and a valid club
        with points,
        When posting a request to /purchase_places
        with requested places with a negative value,
        Then it should display an error message indicating
        that the input is incorrect.
        """
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
        """Given a valid competition and a valid club
        with points,
        When posting a request to /purchase_places
        with requested places with zero value,
        Then it should display an error message indicating
        that the input is incorrect.
        """
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
        """Given a valid competition and a valid club
        with points,
        When posting a request to /purchase_places
        with requested places above 12,
        Then it should display an error message indicating
        that the booking quantity is not allowed.
        """
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
        """Given a valid past competition and a valid club
        with points,
        When posting a request to /purchase_places,
        Then it should display an error message indicating
        that booking in a past competition is impossible.
        """
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

    def test_club_without_point_cannot_purchase(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_dummy_club,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        """Given a valid competition and a valid club
        without points,
        When posting a request to /purchase_places,
        Then it should display an error message indicating
        that the club does not have enough points to book places.
        """
        places_booked = 5
        data = {
            "competition": "Spring Festival",
            "club": "Dummy Club",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert (
            "You do not have enough points to book places."
            in response.data.decode()
        )

    def test_purchase_places_with_invalid_club(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_none,
        monkey_helper_get_competition_returns_spring_festival,
    ):
        """Given a valid competition and an invalid club,
        When posting a request to /purchase_places,
        Then it should display an error message indicating
        that the booking is invalid.
        """
        places_booked = 5
        data = {
            "competition": "Spring Festival",
            "club": "Wrong Club",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert (
            "book if the competition or the account is invalid. Please try again."
            in response.data.decode()
        )

    def test_purchase_places_with_invalid_competition(
        self,
        client,
        monkey_clubs,
        monkey_competitions,
        monkey_helper_get_club_via_name_returns_simply_lift,
        monkey_helper_get_competition_returns_none,
    ):
        """Given a invalid competition and a valid club,
        When posting a request to /purchase_places,
        Then it should display an error message indicating
        that the booking is invalid.
        """
        places_booked = 5
        data = {
            "competition": "Wrong Competition",
            "club": "Simply Lift",
            "places": places_booked,
        }

        response = client.post("/purchase_places", data=data)

        assert (
            "book if the competition or the account is invalid. Please try again."
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
        self,
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
        self,
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
        self,
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
        self,
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
        """Given a valid past competition and a valid club,
        When accessing the /book route,
        Then it should display an error message indicating
        that booking in a past competition is impossible.
        """
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
        """Given valid club data,
        When accessing the /points route,
        Then it should return a page displaying a table showing
        all the clubs with their current points.
        """
        response = client.get(f"/points")

        assert "Registered clubs' points to date" in response.data.decode()

    def test_points_page_show_existing_club_name(self, client, monkey_clubs):
        """Given valid club data,
        When accessing the /points route,
        Then it should return a page displaying a table showing
        all existing the clubs name.
        """
        response = client.get(f"/points")

        assert "She Lifts" in response.data.decode()

    def test_points_page_show_existing_club_points(self, client, monkey_clubs):
        """Given valid club data,
        When accessing the /points route,
        Then it should return a page displaying a table showing
        all existing the clubs points.
        """
        response = client.get(f"/points")

        assert "12" in response.data.decode()

    def test_points_page_does_not_show_invalid_club(
        self, client, monkey_clubs
    ):
        """Given valid club data,
        When accessing the /points route,
        Then it should return a page displaying a table showing
        only clubs in the database.
        """
        response = client.get(f"/points")

        assert "Fake Club" not in response.data.decode()

    def test_points_page_does_not_show_invalid_club_points(
        self, client, monkey_clubs
    ):
        """Given valid club data,
        When accessing the /points route,
        Then it should return a page displaying a table showing
        correct point value for each club.
        """
        response = client.get(f"/points")

        assert "5000" not in response.data.decode()

    def test_points_page_does_not_show_without_clubs(
        self, client, monkey_incorrect_clubs
    ):
        """Given an empty database,
        When accessing the /points route,
        Then it should display a message indicating that
        the page is unavailable.
        """
        response = client.get(f"/points")

        assert "Page unavailable." in response.data.decode()


class TestLogout:
    def test_logout_works(self, client):
        """Given a client,
        When accessing the /logout route,
        Then it should return a status code of 302,
        indicating a successful logout.
        """
        response = client.get(f"/logout")

        response.status_code == 302


class TestIndex:
    def test_index_works(self, client):
        """Given a client,
        When accessing the root route ('/'),
        Then it should display a message asking for
        the secretary's email to continue.
        """
        response = client.get(f"/")

        assert (
            "Please enter your secretary email to continue"
            in response.data.decode()
        )
