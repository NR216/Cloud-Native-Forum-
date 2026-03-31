import os


def _read_secret(name, default=None):
    """Read a Docker Swarm secret from /run/secrets/, fallback to env var."""
    path = f'/run/secrets/{name}'
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.environ.get(name.upper(), default)


def _build_database_url():
    """Build DATABASE_URL, using Docker secret for password if available."""
    url = os.environ.get('DATABASE_URL')
    if url:
        return url
    db_password = _read_secret('db_password', 'forum')
    return f'postgresql://forum:{db_password}@postgres:5432/forum'


class Config:
    SECRET_KEY = _read_secret('secret_key', 'dev-secret-key-change-me')
    DATABASE_URL = _build_database_url()
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # Flask-Session with Redis
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_KEY_PREFIX = 'forum:'

    # Admin defaults
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

    # Backup
    BACKUP_DIR = os.environ.get('BACKUP_DIR', '/backups')

    @staticmethod
    def init_app(app):
        import redis as redis_lib
        app.config['SESSION_REDIS'] = redis_lib.from_url(app.config['REDIS_URL'])
