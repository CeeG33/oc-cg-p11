import server


def test_index_works(client):
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