from flask import Flask
from app.views import RegisterView, GameView, ResetView, HighScoresView
from app.extensions import db
from app.helper import initialize_fixtures


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    # db.drop_all(app=app)
    db.create_all(app=app)
    # initialize_fixtures(db)

    app.add_url_rule('/', view_func=RegisterView.as_view('register'))
    app.add_url_rule('/game-on/', view_func=GameView.as_view('game'))
    app.add_url_rule('/reset/', view_func=ResetView.as_view('reset'))
    app.add_url_rule('/high_scores/', view_func=HighScoresView.as_view('high_scores'))
    return app


