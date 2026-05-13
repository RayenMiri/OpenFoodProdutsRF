import os
import pytest
from app import create_app
from extensions import db as _db

TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///:memory:"
    ),
    "RATELIMIT_ENABLED": False,
}


@pytest.fixture(scope="session")
def app():
    application = create_app(TEST_CONFIG)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()
