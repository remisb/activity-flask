import os
import tempfile
import pytest
from activity import create_app


@pytest.fixture
def client():
    db_fd, db_file = tempfile.mkstemp()
    app = create_app(settings={
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
