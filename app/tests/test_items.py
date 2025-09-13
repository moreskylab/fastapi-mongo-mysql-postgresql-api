import pytest
from fastapi.testclient import TestClient


def test_create_item(client: TestClient):
    """Test creating a new item."""
    response = client.post("/items/", json={"name": "Test Item", "description": "A test item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert "id" in data


def test_get_item(client: TestClient):
    """Test retrieving an item by ID."""
    # First create an item
    create_response = client.post("/items/", json={"name": "Get Test Item", "description": "For retrieval"})
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    
    # Then retrieve it
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Get Test Item"
    assert data["description"] == "For retrieval"
    assert data["id"] == item_id


def test_get_nonexistent_item(client: TestClient):
    """Test retrieving a non-existent item returns 404."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_api_docs_accessible(client: TestClient):
    """Test that API documentation is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "FastAPI Template Starter"
    assert "/items/" in data["paths"]