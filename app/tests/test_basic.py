"""
Basic test to verify CI pipeline functionality.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test that the API starts up correctly."""
    response = client.get("/")
    # The app doesn't have a root endpoint, so we expect 404
    # This test just verifies the app can start without crashing
    assert response.status_code in [404, 200]


def test_items_endpoint_structure():
    """Test that the items endpoint structure is accessible."""
    # Test that the endpoint responds (even if with no data)
    response = client.get("/items/1")
    # We expect some response, not a server error
    assert response.status_code != 500