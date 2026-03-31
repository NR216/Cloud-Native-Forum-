import os
import pytest

os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('DATABASE_URL', 'postgresql://forum:forum@localhost:5432/forum_test')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
os.environ.setdefault('TESTING', '1')
os.environ.setdefault('RATELIMIT_ENABLED', 'false')


@pytest.fixture(scope='session')
def app():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """Provide a clean database for each test."""
    from app.database import get_db, pool

    with app.app_context():
        conn = pool.getconn()
        cur = conn.cursor()

        # Clean tables before each test
        cur.execute('DELETE FROM likes')
        cur.execute('DELETE FROM replies')
        cur.execute('DELETE FROM posts')
        cur.execute('DELETE FROM users')
        conn.commit()
        pool.putconn(conn)

        yield

        # Clean up after test
        conn = pool.getconn()
        cur = conn.cursor()
        cur.execute('DELETE FROM likes')
        cur.execute('DELETE FROM replies')
        cur.execute('DELETE FROM posts')
        cur.execute('DELETE FROM users')
        conn.commit()
        pool.putconn(conn)
