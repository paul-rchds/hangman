import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD', 'postgres')}@postgres/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY', 'secret')
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

