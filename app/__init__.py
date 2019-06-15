from flask import Flask
from app import urls
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    db.create_all(app=app)

    app.register_blueprint(urls.register_bp)
    app.register_blueprint(urls.game_bp)
    app.register_blueprint(urls.high_scores_bp)
    app.register_blueprint(urls.reset_bp)
    return app


