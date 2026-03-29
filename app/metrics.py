import time

from flask import Blueprint, g, request
from prometheus_client import (
    Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
)

from app.database import get_cursor

metrics_bp = Blueprint('metrics', __name__)

# --- Prometheus metrics ---
REQUEST_COUNT = Counter(
    'flask_request_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'flask_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)
ACTIVE_CONNECTIONS = Gauge(
    'forum_active_websocket_connections',
    'Number of active WebSocket connections'
)
POSTS_TOTAL = Gauge(
    'forum_posts_total',
    'Total number of posts in the forum'
)
REPLIES_TOTAL = Gauge(
    'forum_replies_total',
    'Total number of replies in the forum'
)
USERS_TOTAL = Gauge(
    'forum_users_total',
    'Total number of registered users'
)
LIKES_TOTAL = Gauge(
    'forum_likes_total',
    'Total number of likes in the forum'
)


def init_metrics(app):
    """Register before/after request hooks for metrics collection."""

    @app.before_request
    def _start_timer():
        g.start_time = time.time()

    @app.after_request
    def _record_metrics(response):
        if request.endpoint == 'metrics.metrics_endpoint':
            return response

        latency = time.time() - g.get('start_time', time.time())
        endpoint = request.endpoint or 'unknown'

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(latency)

        return response


def _update_gauges():
    """Update gauge metrics with current database counts."""
    try:
        cur = get_cursor()
        cur.execute('SELECT COUNT(*) AS cnt FROM posts')
        POSTS_TOTAL.set(cur.fetchone()['cnt'])

        cur.execute('SELECT COUNT(*) AS cnt FROM replies')
        REPLIES_TOTAL.set(cur.fetchone()['cnt'])

        cur.execute('SELECT COUNT(*) AS cnt FROM users')
        USERS_TOTAL.set(cur.fetchone()['cnt'])

        cur.execute('SELECT COUNT(*) AS cnt FROM likes')
        LIKES_TOTAL.set(cur.fetchone()['cnt'])
    except Exception:
        pass


@metrics_bp.route('/metrics')
def metrics_endpoint():
    _update_gauges()
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
