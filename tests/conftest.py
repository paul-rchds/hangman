import pytest
from app import create_app
from app.extensions import db
from sqlalchemy_utils import database_exists, create_database
from config import DATABASE_URI_TEMPLATE

LOGIN_DATA = {'username': 'Paul'}


@pytest.fixture
def app():
    SQLALCHEMY_DATABASE_URI = DATABASE_URI_TEMPLATE.format(db='test')

    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI
    })

    with app.app_context():
        pass

    yield app

    db.drop_all(app=app)


@pytest.fixture
def client(app):
    return app.test_client()
