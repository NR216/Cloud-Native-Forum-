from flask import (
    Blueprint, request, redirect, url_for,
    session, jsonify
)

from app.database import get_db, get_cursor
from app.auth import login_required, _is_ajax
from app import socketio

likes_bp = Blueprint('likes', __name__)


@likes_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    db = get_db()
    cur = get_cursor()
    user_id = session['user_id']

    cur.execute(
        'SELECT id FROM likes WHERE post_id = %s AND user_id = %s',
        (post_id, user_id)
    )
    existing = cur.fetchone()

    if existing:
        cur.execute('DELETE FROM likes WHERE id = %s', (existing['id'],))
        liked = False
    else:
        cur.execute(
            'INSERT INTO likes (post_id, user_id) VALUES (%s, %s)',
            (post_id, user_id)
        )
        liked = True
    db.commit()

    cur.execute(
        'SELECT COUNT(*) AS cnt FROM likes WHERE post_id = %s', (post_id,)
    )
    like_count = cur.fetchone()['cnt']

    socketio.emit('like_update', {
        'post_id': post_id,
        'like_count': like_count,
    })

    if _is_ajax():
        return jsonify({'success': True, 'liked': liked, 'like_count': like_count})

    return redirect(url_for('posts.view_post', post_id=post_id))
