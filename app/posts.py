import os
import uuid

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify, abort, current_app, send_from_directory
)
from werkzeug.utils import secure_filename

from app.database import get_db, get_cursor
from app.auth import login_required, admin_required, _is_ajax
from app import socketio, limiter

posts_bp = Blueprint('posts', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = '/app/uploads'


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_upload(file):
    """Save an uploaded file and return the URL path."""
    if not file or file.filename == '':
        return None
    if not _allowed_file(file.filename):
        return None

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{uuid.uuid4().hex}.{ext}'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return f'/uploads/{filename}'


@posts_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(UPLOAD_FOLDER, filename)


@posts_bp.route('/')
def index():
    cur = get_cursor()
    cur.execute('''
        SELECT p.*, u.username AS author_name,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.id) AS like_count,
               (SELECT COUNT(*) FROM replies WHERE post_id = p.id) AS reply_count
        FROM posts p
        JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC
    ''')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@posts_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
@limiter.limit("10 per minute", methods=["POST"])
def create_post():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        is_anonymous = request.form.get('is_anonymous') == 'on'

        if not title or not content:
            if _is_ajax():
                return jsonify({'error': 'Title and content are required.'}), 400
            flash('Title and content are required.', 'danger')
            return render_template('create_post.html')

        # Handle image upload
        image_url = None
        if 'image' in request.files:
            image_url = _save_upload(request.files['image'])

        db = get_db()
        cur = get_cursor()
        cur.execute(
            '''INSERT INTO posts (title, content, image_url, is_anonymous, author_id)
               VALUES (%s, %s, %s, %s, %s) RETURNING id''',
            (title, content, image_url, is_anonymous, session['user_id'])
        )
        post_id = cur.fetchone()['id']
        db.commit()

        cur.execute(
            '''SELECT p.*, u.username AS author_name
               FROM posts p JOIN users u ON p.author_id = u.id
               WHERE p.id = %s''',
            (post_id,)
        )
        post = cur.fetchone()

        display_name = 'Anonymous' if is_anonymous else post['author_name']

        socketio.emit('new_post', {
            'id': post['id'],
            'title': post['title'],
            'content': post['content'],
            'image_url': image_url or '',
            'is_anonymous': is_anonymous,
            'author_name': display_name,
            'created_at': str(post['created_at']),
            'like_count': 0,
            'reply_count': 0,
        })

        if _is_ajax():
            return jsonify({'success': True, 'post_id': post_id})

        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.index'))

    return render_template('create_post.html')


@posts_bp.route('/post/<int:post_id>')
def view_post(post_id):
    cur = get_cursor()
    cur.execute('''
        SELECT p.*, u.username AS author_name,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.id) AS like_count
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.id = %s
    ''', (post_id,))
    post = cur.fetchone()

    if post is None:
        abort(404)

    cur.execute('''
        SELECT r.*, u.username AS author_name
        FROM replies r
        JOIN users u ON r.author_id = u.id
        WHERE r.post_id = %s
        ORDER BY r.created_at ASC
    ''', (post_id,))
    replies = cur.fetchall()

    user_liked = False
    if 'user_id' in session:
        cur.execute(
            'SELECT id FROM likes WHERE post_id = %s AND user_id = %s',
            (post_id, session['user_id'])
        )
        user_liked = cur.fetchone() is not None

    return render_template('post_detail.html', post=post, replies=replies, user_liked=user_liked)


@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete_post(post_id):
    db = get_db()
    cur = get_cursor()
    cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
    db.commit()

    socketio.emit('delete_post', {'post_id': post_id})

    if _is_ajax():
        return jsonify({'success': True})

    flash('Post deleted.', 'info')
    return redirect(url_for('posts.index'))
