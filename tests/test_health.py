from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "environment" in data


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


def test_readiness_check(client: TestClient):
    """Test readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "version" in data
    assert "environment" in data
    assert "database" in data


def test_metrics_endpoint(client: TestClient):
    """Test Prometheus metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


def test_example_items_list(client: TestClient):
    """Test listing items."""
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_example_item_crud(client: TestClient, sample_item):
    """Test CRUD operations for items."""
    # Create item
    response = client.post("/api/items", json=sample_item)
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["name"] == sample_item["name"]
    assert created_item["price"] == sample_item["price"]
    item_id = created_item["id"]

    # Get item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    retrieved_item = response.json()
    assert retrieved_item["id"] == item_id
    assert retrieved_item["name"] == sample_item["name"]

    # Update item
    update_data = {"name": "Updated Item", "price": 19.99}
    response = client.put(f"/api/items/{item_id}", json=update_data)
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["name"] == "Updated Item"
    assert updated_item["price"] == 19.99

    # Delete item
    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"

    # Verify item is deleted
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 404


def test_get_nonexistent_item(client: TestClient):
    """Test getting a non-existent item."""
    response = client.get("/api/items/999")
    assert response.status_code == 404
