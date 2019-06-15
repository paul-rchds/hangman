import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def test_app():

    app = create_app({
        'TESTING': True,
        # 'SQLALCHEMY_DATABASE_URI': f'sqlite:///test.db',
    })

    print(app.config)

    yield app

    db.drop_all(app=app)


@pytest.fixture
def client(test_app):
    return test_app.test_client()
