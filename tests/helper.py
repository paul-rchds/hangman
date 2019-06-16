import json
from app.constants import STATUS_OK
from tests.conftest import LOGIN_DATA
from app.models import Game


def register(client):
    return client.post('/', data=LOGIN_DATA, follow_redirects=True)


def register_api(client):
    return client.post('/api/', data=json.dumps(LOGIN_DATA), follow_redirects=True)


def parse_json(data):
    return json.loads(data.decode())


def is_status_okay(data):
    parsed_data = parse_json(data)
    status = parsed_data.get('status', '')

    if status == STATUS_OK:
        return True
    else:
        return False


def win_game(client):
    with client:
        register(client)
        client.get('/game/')
        game = Game.query.get(1)
        for letter in list(game.answer):
            response = client.post('/game/api/', data=json.dumps({'letter': letter}))
            if b'Well done, you have won' in response.data:
                return response

        return response


def loose_game(client):
    loose_letters = '09876'  # FIXME: Should get characters that are definitely not in the answer.
    register(client)
    client.get('/game/')

    for letter in list(loose_letters):
        response = client.post('/game/api/', data=json.dumps({'letter': letter}))

    return response
