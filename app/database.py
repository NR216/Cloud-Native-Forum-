import psycopg2
import psycopg2.pool
import psycopg2.extras
from flask import g

pool = None


def init_pool(app):
    """Initialize the PostgreSQL connection pool."""
    global pool
    pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=2,
        maxconn=10,
        dsn=app.config['DATABASE_URL']
    )


def get_db():
    """Get a database connection from the pool for the current request."""
    if 'db' not in g:
        g.db = pool.getconn()
    return g.db


def get_cursor():
    """Get a RealDictCursor for the current request's connection."""
    db = get_db()
    return db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def close_db(exc=None):
    """Return the connection to the pool at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        if exc is not None:
            db.rollback()
        pool.putconn(db)


def init_db(app):
    """Run the schema migration and create default admin account."""
    import os
    from werkzeug.security import generate_password_hash

    conn = pool.getconn()
    try:
        cur = conn.cursor()

        # Run init.sql schema
        sql_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'migrations', 'init.sql'
        )
        with open(sql_path, 'r') as f:
            cur.execute(f.read())

        # Create default admin if not exists
        cur.execute('SELECT id FROM users WHERE username = %s',
                    (app.config['ADMIN_USERNAME'],))
        if cur.fetchone() is None:
            cur.execute(
                'INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                (
                    app.config['ADMIN_USERNAME'],
                    generate_password_hash(app.config['ADMIN_PASSWORD']),
                    'admin'
                )
            )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)
