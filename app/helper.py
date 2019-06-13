from flask import session
from app.constants import IN_PROGRESS
from app.models import User, Game


def get_or_create_game(user):
    game_in_progress = user.games.filter_by(status=IN_PROGRESS).first()

    if game_in_progress:
        return game_in_progress
    else:
        new_game = Game(user_id=user.id)
        new_game.start_new_game()
        return new_game


def get_user():
    user_id = session.get('user_id')
    return User.query.filter_by(id=user_id).first()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance



