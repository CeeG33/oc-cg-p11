import pytest
from server import app
from tests.conftest import client, clubs


class TestShowSummary:   
    def test_show_summary_with_existing_email(self, client, clubs):
        app.config["clubs"] = clubs
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        
        assert b"john@simplylift.co" in response.data
        
    def test_login_with_invalid_email(self, client, clubs):
        app.config["clubs"] = clubs
        response = client.post("/showSummary", data={"email": "wrong@email.com"})
        
        assert b"Email not found. Please try a valid email." in response.data