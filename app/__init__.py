from flask import Flask
from app.views import RegisterView, GameView, ResetView, HighScoresView
from app.extensions import db
# from database import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # init_db()

    app.add_url_rule('/', view_func=RegisterView.as_view('register'))
    app.add_url_rule('/game-on/', view_func=GameView.as_view('game'))
    app.add_url_rule('/reset/', view_func=ResetView.as_view('reset'))
    app.add_url_rule('/high_scores/', view_func=HighScoresView.as_view('high_scores'))
    return app


