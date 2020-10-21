import os
import tempfile
import pytest
import activity

# from activity import create_app

db_fd = None


def create_app():
    """Return Flask's app object with test configuration"""
    global db_fd
    db_fd, db_file = tempfile.mkstemp()

    app = activity.create_app(config_name='testing',
                              settings={
                                  'SQLALCHEMY_TRACK_MODIFICATIONS': False,
                                  'DATABASE': db_file,
                                  'TESTING': True,
                                  'JWT_SECRET_KEY':  'convious-secret'
                              })

    app.config.from_object("activity.config.TestingConfig")
    return app


def set_up():
    """Create database tables according to the app models"""
    # db.create_all()
    # db.session.commit()
    pass


def tear_down():
    """Remove all tables from the database"""
    activity.db.session.remove()
    activity.db.drop_all()


@pytest.fixture
def client007():
    db_fd, db_file = tempfile.mkstemp()
    app = create_app({
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DATABASE': db_file,
        'TESTING': True,
        'JWT_SECRET_KEY':  'convious-secret'
    })
    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    # app.config['TESTING'] = True

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def db():
    app = create_app()
    db = activity.db

    yield db

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def client():
    """Create Flask's test client to interact with the application"""
    app = create_app()
    client = app.test_client()
    set_up()
    yield client
    # tear_down()

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
