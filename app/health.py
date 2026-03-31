from flask import Blueprint, jsonify

from app.database import get_db, get_cursor

health_bp = Blueprint('health', __name__)


@health_bp.route('/health')
def health():
    checks = {}

    # Check PostgreSQL
    try:
        cur = get_cursor()
        cur.execute('SELECT 1')
        cur.fetchone()
        checks['database'] = 'healthy'
    except Exception as e:
        checks['database'] = f'unhealthy: {str(e)}'

    # Check Redis
    try:
        from flask import current_app
        import redis
        r = redis.from_url(current_app.config['REDIS_URL'])
        r.ping()
        checks['redis'] = 'healthy'
    except Exception as e:
        checks['redis'] = f'unhealthy: {str(e)}'

    healthy = all(v == 'healthy' for v in checks.values())
    status_code = 200 if healthy else 503

    return jsonify({
        'status': 'healthy' if healthy else 'unhealthy',
        'checks': checks
    }), status_code
