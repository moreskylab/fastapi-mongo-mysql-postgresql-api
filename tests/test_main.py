import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "databases" in data
    assert "MongoDB" in data["databases"]
    assert "MySQL" in data["databases"]
    assert "PostgreSQL" in data["databases"]


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


def test_mongodb_users_endpoint():
    """Test MongoDB users endpoint is accessible"""
    response = client.get("/api/v1/mongodb/users/")
    # Should return 200 or 500/503 (if MongoDB is not available)
    assert response.status_code in [200, 500, 503]


def test_mysql_users_endpoint():
    """Test MySQL users endpoint is accessible"""
    response = client.get("/api/v1/mysql/users/")
    # Should return 200 or 500 (if MySQL is not available)
    assert response.status_code in [200, 500]


def test_postgresql_users_endpoint():
    """Test PostgreSQL users endpoint is accessible"""
    response = client.get("/api/v1/postgresql/users/")
    # Should return 200 or 500 (if PostgreSQL is not available)
    assert response.status_code in [200, 500]