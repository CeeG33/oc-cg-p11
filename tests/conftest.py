import pytest

import server
from server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()
    
@pytest.fixture
def clubs():
    clubs = [
        {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        },
        {
            "name":"Iron Temple",
            "email": "admin@irontemple.com",
            "points":"4"
        },
        {   "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"12"
        }
    ]
    
    return clubs