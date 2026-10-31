"""
Test Health Endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.unit
def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["name"] == "AUREX"


@pytest.mark.unit
def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "environment" in data
    assert "services" in data
    assert data["status"] == "healthy"


@pytest.mark.unit
def test_health_endpoint_structure():
    """Test health endpoint response structure"""
    response = client.get("/api/health")
    data = response.json()
    
    # Check required fields
    required_fields = ["status", "version", "environment", "timestamp", "services"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check services is a dictionary
    assert isinstance(data["services"], dict)
