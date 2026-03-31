from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

socketio = SocketIO()
sess = Session()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per minute"])


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize Redis-backed sessions
    from app.config import Config
    Config.init_app(app)
    sess.init_app(app)

    # Initialize rate limiter with Redis storage
    limiter.init_app(app)
    app.config['RATELIMIT_STORAGE_URI'] = app.config['REDIS_URL']

    # Initialize SocketIO with Redis message queue (for multi-replica broadcast)
    socketio.init_app(
        app,
        message_queue=app.config['REDIS_URL'],
        async_mode='eventlet',
        cors_allowed_origins='*'
    )

    # Initialize database pool
    from app.database import init_pool, init_db, close_db
    init_pool(app)
    init_db(app)
    app.teardown_appcontext(close_db)

    # Register context processor
    @app.context_processor
    def inject_user():
        from flask import session
        if 'user_id' in session:
            return {
                'current_user': {
                    'id': session['user_id'],
                    'username': session['username'],
                    'role': session['role']
                }
            }
        return {'current_user': None}

    # Register blueprints
    from app.auth import auth_bp
    from app.posts import posts_bp
    from app.replies import replies_bp
    from app.likes import likes_bp
    from app.reports import reports_bp
    from app.health import health_bp
    from app.metrics import metrics_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(replies_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(admin_bp)

    return app
