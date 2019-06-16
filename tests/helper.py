import json
from app.constants import STATUS_OK


def parse_json(data):
    return json.loads(data.decode())


def is_status_okay(data):
    parsed_data = parse_json(data)
    status = parsed_data.get('status', '')

    if status == STATUS_OK:
        return True
    else:
        return False