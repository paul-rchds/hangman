from tests.helper import is_status_okay, register, register_api


def test_register_get(client):
    response = client.get('/')
    assert b'Please enter your name' in response.data


def test_register_get_api(client):
    response = client.get('/api/')
    assert is_status_okay(response.data)


def test_register_post(client):
    response = register(client)
    assert b'Please enter a letter' in response.data


def test_register_post_api(client):
    response = register_api(client)
    assert is_status_okay(response.data)




