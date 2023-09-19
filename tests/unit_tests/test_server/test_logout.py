import server


def test_logout_works(client):
    """Given a client,
    When accessing the /logout route,
    Then it should return a status code of 302,
    indicating a successful logout.
    """
    response = client.get(f"/logout")

    response.status_code == 302