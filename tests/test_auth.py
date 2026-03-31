"""Tests for authentication routes."""


def test_register_page_loads(client):
    """Test that the register page loads successfully."""
    resp = client.get('/register')
    assert resp.status_code == 200
    assert b'Register' in resp.data


def test_login_page_loads(client):
    """Test that the login page loads successfully."""
    resp = client.get('/login')
    assert resp.status_code == 200
    assert b'Login' in resp.data


def test_register_and_login(client, db):
    """Test user registration and login flow."""
    # Register a new user
    resp = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass',
        'confirm_password': 'testpass'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Registration successful' in resp.data

    # Login with the new user
    resp = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Welcome, testuser' in resp.data


def test_register_password_mismatch(client, db):
    """Test that mismatched passwords are rejected."""
    resp = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass',
        'confirm_password': 'wrongpass'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Passwords do not match' in resp.data


def test_register_short_password(client, db):
    """Test that short passwords are rejected."""
    resp = client.post('/register', data={
        'username': 'testuser',
        'password': 'abc',
        'confirm_password': 'abc'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'at least 4 characters' in resp.data


def test_register_duplicate_username(client, db):
    """Test that duplicate usernames are rejected."""
    # Register first user
    client.post('/register', data={
        'username': 'duplicate',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    # Try to register with the same username
    resp = client.post('/register', data={
        'username': 'duplicate',
        'password': 'testpass',
        'confirm_password': 'testpass'
    }, follow_redirects=True)
    assert b'Username already taken' in resp.data


def test_login_invalid_credentials(client, db):
    """Test that invalid credentials are rejected."""
    resp = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Invalid username or password' in resp.data


def test_logout(client, db):
    """Test the logout flow."""
    # Register and login
    client.post('/register', data={
        'username': 'logoutuser',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'logoutuser',
        'password': 'testpass'
    })

    # Logout
    resp = client.get('/logout', follow_redirects=True)
    assert resp.status_code == 200
    assert b'You have been logged out' in resp.data
