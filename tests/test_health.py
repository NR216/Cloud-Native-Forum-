"""Tests for health check endpoint."""


def test_health_endpoint(client):
    """Test that the health endpoint returns status."""
    resp = client.get('/health')
    data = resp.get_json()
    assert 'status' in data
    assert 'checks' in data
    assert 'database' in data['checks']
    assert 'redis' in data['checks']
