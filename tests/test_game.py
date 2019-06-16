import json
from tests.conftest import LOGIN_DATA
from tests.helper import parse_json, is_status_okay
from tests.helper import register_api, register, win_game, loose_game


def test_game_get(client):
    response = client.get('/game/')
    assert response.status_code == 302


def test_game_get_api(client):
    response = client.get('/game/api/')
    assert response.status_code == 302


def test_game_get_with_session(client):
    register(client)
    response = client.get('/game/')
    assert response.status_code == 200
    assert b'Incorrect guesses:' in response.data


def test_game_get_with_session_api(client):
    register_api(client)
    response = client.get('/game/api/')
    data = parse_json(response.data)
    assert response.status_code == 200
    assert is_status_okay(response.data)
    assert 'game' in data
    assert data['user']['username'] == LOGIN_DATA['username']
    assert data['game']['incorrect_count'] == 0
    assert data['game']['turn_count'] == 0


def test_game_win(client):
    response = win_game(client)
    data = parse_json(response.data)
    assert is_status_okay(response.data)
    assert b'Well done, you have won' in response.data
    assert data['game']['incorrect_count'] == 0


def test_game_lose(client):
    response = loose_game(client)
    data = parse_json(response.data)
    assert b'GAME OVER' in response.data
    assert data['game']['incorrect_count'] == 5


def test_game_input_fail(client):
    register_api(client)
    response = client.post('/game/api/', data=json.dumps({'letter': '@'}))
    assert b'Input should be a single character between A-Z or 0-9' in response.data


def test_game_same_input(client):
    register_api(client)
    client.post('/game/api/', data=json.dumps({'letter': 'R'}))
    response = client.post('/game/api/', data=json.dumps({'letter': 'R'}))
    assert b'You have already guessed the letter' in response.data
