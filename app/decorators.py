from flask import redirect, url_for, g
from app.helper import get_or_create_game, get_user


def wrap_game(func):

    def decorator(*args, **kwargs):
        g.user = get_user()

        if not g.user:
            return redirect(url_for('register'))

        g.game = get_or_create_game(g.user)

        return func(*args, **kwargs)

    return decorator
