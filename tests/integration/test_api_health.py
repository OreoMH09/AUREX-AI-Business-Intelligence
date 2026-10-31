"""
Integration tests for API health endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.integration
class TestHealthAPI:
    """Test suite for health check endpoints"""
    
    def test_health_endpoint(self):
        """Test main health endpoint"""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data
    
    def test_rag_health_endpoint(self):
        """Test RAG system health"""
        response = client.get("/api/rag-health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "vector_store" in data
        assert "llm" in data
        assert "overall" in data
    
    def test_evaluation_health_endpoint(self):
        """Test evaluation system health"""
        response = client.get("/api/evaluation/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "evaluation_active" in data
