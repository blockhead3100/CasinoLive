# tests/test_app.py
import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_user():
    with app.app_context():
        user = User(id=1, username="test_user", password="test_password", balance=100.0, is_admin=False)
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location

def test_blackjack_route(client):
    with client.session_transaction() as session:
        session['user_id'] = 1  # Mock user ID

    response = client.get('/blackjack')
    assert response.status_code == 200
    assert b"Blackjack" in response.data

def test_blackjack_ai_logic(client, mocker, setup_user):
    mocker.patch('openai.Completion.create', return_value=mocker.Mock(choices=[mocker.Mock(text="hit")]))

    with client.session_transaction() as session:
        session['user_id'] = setup_user.id
        session['deck'] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        session['player_hand'] = [10, 7]
        session['dealer_hand'] = [10, 6]

    response = client.post('/blackjack', data={'bet': 10})
    assert response.status_code == 200
    assert b"Dealer" in response.data