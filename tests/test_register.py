

def register(client, username):
    return client.post('/login', data=dict(
        username=username,
    ), follow_redirects=True)


def reset(client):
    return client.get('/login', follow_redirects=True)


def test_register(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Please enter your name' in response.data