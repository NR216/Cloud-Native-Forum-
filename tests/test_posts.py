"""Tests for post-related routes."""


def _register_and_login(client, username='testuser', password='testpass'):
    """Helper: register and login a user."""
    client.post('/register', data={
        'username': username,
        'password': password,
        'confirm_password': password
    })
    client.post('/login', data={
        'username': username,
        'password': password
    })


def test_index_page_loads(client):
    """Test that the index page loads."""
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'All Posts' in resp.data


def test_create_post_requires_login(client):
    """Test that creating a post requires login."""
    resp = client.get('/post/new', follow_redirects=True)
    assert b'Please log in first' in resp.data


def test_create_and_view_post(client, db):
    """Test creating a post and viewing it."""
    _register_and_login(client)

    # Create a post via AJAX
    resp = client.post('/post/new', data={
        'title': 'Test Post',
        'content': 'This is test content.'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    post_id = data['post_id']

    # View the post
    resp = client.get(f'/post/{post_id}')
    assert resp.status_code == 200
    assert b'Test Post' in resp.data
    assert b'This is test content.' in resp.data


def test_create_post_empty_fields(client, db):
    """Test that empty fields are rejected."""
    _register_and_login(client)

    resp = client.post('/post/new', data={
        'title': '',
        'content': 'Some content'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_view_nonexistent_post(client):
    """Test viewing a post that doesn't exist returns 404."""
    resp = client.get('/post/99999')
    assert resp.status_code == 404


def test_post_appears_on_index(client, db):
    """Test that a created post appears on the index page."""
    _register_and_login(client)

    client.post('/post/new', data={
        'title': 'Visible Post',
        'content': 'Should appear on index.'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})

    resp = client.get('/')
    assert b'Visible Post' in resp.data
