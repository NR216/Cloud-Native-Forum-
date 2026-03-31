from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import get_db, get_cursor
from app import limiter

auth_bp = Blueprint('auth', __name__)


def _is_ajax():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if _is_ajax():
                return jsonify({'error': 'Login required'}), 401
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if _is_ajax():
                return jsonify({'error': 'Login required'}), 401
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            if _is_ajax():
                return jsonify({'error': 'Forbidden'}), 403
            from flask import abort
            abort(403)
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=["POST"])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm = request.form['confirm_password']

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('register.html')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        if len(password) < 4:
            flash('Password must be at least 4 characters.', 'danger')
            return render_template('register.html')

        db = get_db()
        cur = get_cursor()
        cur.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cur.fetchone():
            flash('Username already taken.', 'danger')
            return render_template('register.html')

        cur.execute(
            'INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
            (username, generate_password_hash(password), 'user')
        )
        db.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        cur = get_cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome, {user["username"]}!', 'success')
            return redirect(url_for('posts.index'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('posts.index'))
