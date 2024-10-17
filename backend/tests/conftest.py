import pytest
import os
import sys
from sqlalchemy.orm import sessionmaker, scoped_session
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    yield _db

@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, **options))

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture()
def client(app):
    return app.test_client()