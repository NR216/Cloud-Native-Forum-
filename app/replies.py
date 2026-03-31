from flask import (
    Blueprint, request, redirect, url_for,
    flash, session, jsonify
)

from app.database import get_db, get_cursor
from app.auth import login_required, admin_required, _is_ajax
from app import socketio

replies_bp = Blueprint('replies', __name__)


@replies_bp.route('/post/<int:post_id>/reply', methods=['POST'])
@login_required
def add_reply(post_id):
    content = request.form['content'].strip()
    is_anonymous = request.form.get('is_anonymous') == 'on'
    if not content:
        if _is_ajax():
            return jsonify({'error': 'Reply cannot be empty.'}), 400
        flash('Reply cannot be empty.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))

    db = get_db()
    cur = get_cursor()
    cur.execute(
        '''
        INSERT INTO replies (content, is_anonymous, post_id, author_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        ''',
        (content, is_anonymous, post_id, session['user_id'])
    )
    reply_id = cur.fetchone()['id']
    db.commit()

    cur.execute(
        '''SELECT r.*,
                  CASE WHEN r.is_anonymous THEN 'Anonymous' ELSE u.username END AS author_name
           FROM replies r JOIN users u ON r.author_id = u.id
           WHERE r.id = %s''',
        (reply_id,)
    )
    reply = cur.fetchone()

    cur.execute(
        'SELECT COUNT(*) AS cnt FROM replies WHERE post_id = %s', (post_id,)
    )
    reply_count = cur.fetchone()['cnt']

    socketio.emit('new_reply', {
        'id': reply['id'],
        'content': reply['content'],
        'author_name': reply['author_name'],
        'is_anonymous': reply['is_anonymous'],
        'created_at': str(reply['created_at']),
        'post_id': post_id,
        'reply_count': reply_count,
    })

    if _is_ajax():
        return jsonify({'success': True, 'reply_id': reply_id})

    flash('Reply posted!', 'success')
    return redirect(url_for('posts.view_post', post_id=post_id))


@replies_bp.route('/post/<int:post_id>/reply/<int:reply_id>/delete', methods=['POST'])
@admin_required
def delete_reply(post_id, reply_id):
    db = get_db()
    cur = get_cursor()
    cur.execute('DELETE FROM replies WHERE id = %s', (reply_id,))
    db.commit()

    cur.execute(
        'SELECT COUNT(*) AS cnt FROM replies WHERE post_id = %s', (post_id,)
    )
    reply_count = cur.fetchone()['cnt']

    socketio.emit('delete_reply', {
        'reply_id': reply_id,
        'post_id': post_id,
        'reply_count': reply_count,
    })

    if _is_ajax():
        return jsonify({'success': True})

    flash('Reply deleted.', 'info')
    return redirect(url_for('posts.view_post', post_id=post_id))
