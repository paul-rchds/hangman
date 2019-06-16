from tests.helper import parse_json, is_status_okay
import json

LOGIN_DATA = {'username': 'Paul'}


def test_register_get(client):
    response = client.get('/')
    assert b'Please enter your name' in response.data


def test_register_get_api(client):
    response = client.get('/api/')
    assert is_status_okay(response.data)


def test_register_post(client):
    response = client.post('/', data=LOGIN_DATA, follow_redirects=True)
    assert b'Playing  game as' in response.data


def test_register_post_api(client):
    response = client.post('/api/', data=json.dumps(LOGIN_DATA), follow_redirects=True)
    print(response.data)
    assert is_status_okay(response.data)




