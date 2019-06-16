import os

DATABASE_URI_TEMPLATE = f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD', 'postgres')}@postgres/{{db}}"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = DATABASE_URI_TEMPLATE.format(db='postgres')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

