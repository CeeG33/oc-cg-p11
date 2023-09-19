import server


def test_points_page_works(client, monkey_clubs):
    """Given valid club data,
    When accessing the /points route,
    Then it should return a page displaying a table showing
    all the clubs with their current points.
    """
    response = client.get(f"/points")

    assert "Registered clubs' points to date" in response.data.decode()

def test_points_page_show_existing_club_name(client, monkey_clubs):
    """Given valid club data,
    When accessing the /points route,
    Then it should return a page displaying a table showing
    all existing the clubs name.
    """
    response = client.get(f"/points")

    assert "She Lifts" in response.data.decode()

def test_points_page_show_existing_club_points(client, monkey_clubs):
    """Given valid club data,
    When accessing the /points route,
    Then it should return a page displaying a table showing
    all existing the clubs points.
    """
    response = client.get(f"/points")

    assert "12" in response.data.decode()

def test_points_page_does_not_show_invalid_club(
    client, monkey_clubs
):
    """Given valid club data,
    When accessing the /points route,
    Then it should return a page displaying a table showing
    only clubs in the database.
    """
    response = client.get(f"/points")

    assert "Fake Club" not in response.data.decode()

def test_points_page_does_not_show_invalid_club_points(
    client, monkey_clubs
):
    """Given valid club data,
    When accessing the /points route,
    Then it should return a page displaying a table showing
    correct point value for each club.
    """
    response = client.get(f"/points")

    assert "5000" not in response.data.decode()

def test_points_page_does_not_show_without_clubs(
    client, monkey_incorrect_clubs
):
    """Given an empty database,
    When accessing the /points route,
    Then it should display a message indicating that
    the page is unavailable.
    """
    response = client.get(f"/points")

    assert "Page unavailable." in response.data.decode()