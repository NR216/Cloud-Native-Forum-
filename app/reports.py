from flask import (
    Blueprint, request, redirect, url_for,
    flash, session, jsonify
)

from app.database import get_db, get_cursor
from app.auth import login_required, admin_required, _is_ajax
from app import limiter

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/post/<int:post_id>/report', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
def report_post(post_id):
    """Report a post for review by admin."""
    reason = request.form.get('reason', '').strip()
    if not reason:
        if _is_ajax():
            return jsonify({'error': 'Please provide a reason.'}), 400
        flash('Please provide a reason for the report.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))

    db = get_db()
    cur = get_cursor()

    # Check if already reported by this user
    cur.execute(
        'SELECT id FROM reports WHERE post_id = %s AND user_id = %s',
        (post_id, session['user_id'])
    )
    if cur.fetchone():
        if _is_ajax():
            return jsonify({'error': 'You have already reported this post.'}), 400
        flash('You have already reported this post.', 'warning')
        return redirect(url_for('posts.view_post', post_id=post_id))

    cur.execute(
        'INSERT INTO reports (post_id, user_id, reason) VALUES (%s, %s, %s)',
        (post_id, session['user_id'], reason)
    )
    db.commit()

    if _is_ajax():
        return jsonify({'success': True})

    flash('Post reported. An admin will review it.', 'info')
    return redirect(url_for('posts.view_post', post_id=post_id))


@reports_bp.route('/admin/reports')
@admin_required
def view_reports():
    """Admin view: list all reported posts."""
    from flask import render_template
    cur = get_cursor()
    cur.execute('''
        SELECT r.*, u.username AS reporter_name,
               p.title AS post_title, p.id AS post_id,
               pu.username AS post_author
        FROM reports r
        JOIN users u ON r.user_id = u.id
        JOIN posts p ON r.post_id = p.id
        JOIN users pu ON p.author_id = pu.id
        ORDER BY r.created_at DESC
    ''')
    reports = cur.fetchall()
    return render_template('admin_reports.html', reports=reports)


@reports_bp.route('/admin/reports/<int:report_id>/dismiss', methods=['POST'])
@admin_required
def dismiss_report(report_id):
    """Dismiss a report."""
    db = get_db()
    cur = get_cursor()
    cur.execute('DELETE FROM reports WHERE id = %s', (report_id,))
    db.commit()

    if _is_ajax():
        return jsonify({'success': True})

    flash('Report dismissed.', 'info')
    return redirect(url_for('reports.view_reports'))
