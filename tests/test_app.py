# tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirect
    assert '/login' in response.headers['Location']