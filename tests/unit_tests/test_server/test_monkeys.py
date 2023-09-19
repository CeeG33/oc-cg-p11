import server


def test_competitions_returns_monkey(monkey_competitions):
    """Given competitions data is mocked,
    When accessing server.py competitions variable,
    Then it should return the mocked competitions data.
    """
    expected_result = monkey_competitions

    assert server.competitions == expected_result

def test_clubs_returns_monkey(monkey_clubs):
    """Given clubs data is mocked,
    When accessing server.py clubs variable,
    Then it should return the mocked clubs data.
    """
    expected_result = monkey_clubs

    assert server.clubs == expected_result