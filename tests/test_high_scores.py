from tests.helper import win_game, parse_json, is_status_okay


def test_high_scores_none(client):
    response = client.get('/high-scores/api/')
    data = parse_json(response.data)
    assert is_status_okay(response.data)
    assert len(data['results']) == 0


def test_high_scores(client):
    win_game(client)
    response = client.get('/high-scores/api/')
    data = parse_json(response.data)
    assert is_status_okay(response.data)
    assert len(data['results']) == 1


