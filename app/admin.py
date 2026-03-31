from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.security import check_password_hash

from app.database import get_db, get_cursor
from app.auth import admin_required, _is_ajax

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Dedicated admin login page."""
    if 'user_id' in session and session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        cur = get_cursor()
        cur.execute(
            'SELECT * FROM users WHERE username = %s AND role = %s',
            (username, 'admin')
        )
        user = cur.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome, Admin {user["username"]}!', 'success')
            return redirect(url_for('admin.dashboard'))

        flash('Invalid admin credentials.', 'danger')

    return render_template('admin_login.html')


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with system overview."""
    cur = get_cursor()

    # User stats
    cur.execute('SELECT COUNT(*) AS cnt FROM users')
    total_users = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE role = 'admin'")
    total_admins = cur.fetchone()['cnt']

    # Content stats
    cur.execute('SELECT COUNT(*) AS cnt FROM posts')
    total_posts = cur.fetchone()['cnt']
    cur.execute('SELECT COUNT(*) AS cnt FROM replies')
    total_replies = cur.fetchone()['cnt']
    cur.execute('SELECT COUNT(*) AS cnt FROM likes')
    total_likes = cur.fetchone()['cnt']

    # Recent posts
    cur.execute('''
        SELECT p.*, u.username AS author_name,
               (SELECT COUNT(*) FROM replies WHERE post_id = p.id) AS reply_count
        FROM posts p JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC LIMIT 10
    ''')
    recent_posts = cur.fetchall()

    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_admins=total_admins,
                           total_posts=total_posts,
                           total_replies=total_replies,
                           total_likes=total_likes,
                           recent_posts=recent_posts)


@admin_bp.route('/users')
@admin_required
def manage_users():
    """User management page."""
    cur = get_cursor()
    cur.execute('''
        SELECT u.*,
               (SELECT COUNT(*) FROM posts WHERE author_id = u.id) AS post_count,
               (SELECT COUNT(*) FROM replies WHERE author_id = u.id) AS reply_count
        FROM users u ORDER BY u.created_at DESC
    ''')
    users = cur.fetchall()
    return render_template('admin_users.html', users=users)


@admin_bp.route('/users/<int:user_id>/toggle-role', methods=['POST'])
@admin_required
def toggle_role(user_id):
    """Toggle user role between 'user' and 'admin'."""
    if user_id == session['user_id']:
        if _is_ajax():
            return jsonify({'error': 'Cannot change your own role'}), 400
        flash('Cannot change your own role.', 'danger')
        return redirect(url_for('admin.manage_users'))

    db = get_db()
    cur = get_cursor()
    cur.execute('SELECT role FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    if not user:
        if _is_ajax():
            return jsonify({'error': 'User not found'}), 404
        flash('User not found.', 'danger')
        return redirect(url_for('admin.manage_users'))

    new_role = 'admin' if user['role'] == 'user' else 'user'
    cur.execute('UPDATE users SET role = %s WHERE id = %s', (new_role, user_id))
    db.commit()

    if _is_ajax():
        return jsonify({'success': True, 'new_role': new_role})

    flash(f'User role changed to {new_role}.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user and all their content."""
    if user_id == session['user_id']:
        if _is_ajax():
            return jsonify({'error': 'Cannot delete yourself'}), 400
        flash('Cannot delete yourself.', 'danger')
        return redirect(url_for('admin.manage_users'))

    db = get_db()
    cur = get_cursor()

    # Delete user's likes, replies, posts, then the user
    cur.execute('DELETE FROM likes WHERE user_id = %s', (user_id,))
    cur.execute('DELETE FROM replies WHERE author_id = %s', (user_id,))
    cur.execute('DELETE FROM posts WHERE author_id = %s', (user_id,))
    cur.execute('DELETE FROM users WHERE id = %s', (user_id,))
    db.commit()

    if _is_ajax():
        return jsonify({'success': True})

    flash('User deleted.', 'info')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/posts')
@admin_required
def manage_posts():
    """Post management page."""
    cur = get_cursor()
    cur.execute('''
        SELECT p.*, u.username AS author_name,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.id) AS like_count,
               (SELECT COUNT(*) FROM replies WHERE post_id = p.id) AS reply_count
        FROM posts p JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC
    ''')
    posts = cur.fetchall()
    return render_template('admin_posts.html', posts=posts)


@admin_bp.route('/system')
@admin_required
def system_status():
    """System status page with links to monitoring tools."""
    cur = get_cursor()

    # Database stats
    cur.execute("SELECT pg_database_size(current_database()) AS db_size")
    db_size_bytes = cur.fetchone()['db_size']
    db_size_mb = round(db_size_bytes / (1024 * 1024), 2)

    cur.execute("SELECT count(*) AS cnt FROM pg_stat_activity")
    db_connections = cur.fetchone()['cnt']

    # Check Redis
    redis_status = 'unknown'
    try:
        from flask import current_app
        import redis
        r = redis.from_url(current_app.config['REDIS_URL'])
        r.ping()
        redis_info = r.info()
        redis_status = 'healthy'
        redis_memory = redis_info.get('used_memory_human', 'N/A')
        redis_clients = redis_info.get('connected_clients', 'N/A')
    except Exception:
        redis_status = 'unhealthy'
        redis_memory = 'N/A'
        redis_clients = 'N/A'

    return render_template('admin_system.html',
                           db_size_mb=db_size_mb,
                           db_connections=db_connections,
                           redis_status=redis_status,
                           redis_memory=redis_memory,
                           redis_clients=redis_clients)
