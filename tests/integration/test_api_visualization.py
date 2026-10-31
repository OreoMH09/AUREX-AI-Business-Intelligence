"""
Integration tests for Visualization API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.integration
class TestVisualizationAPI:
    """Test suite for visualization endpoints"""
    
    def test_create_chart_endpoint(self):
        """Test chart creation endpoint"""
        response = client.post(
            "/api/visualization/chart",
            json={
                "chart_type": "bar",
                "data": {
                    "x": ["A", "B", "C"],
                    "y": [10, 20, 15]
                },
                "title": "Test Chart"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "chart" in data
        assert data["chart_type"] == "bar"
        assert data["title"] == "Test Chart"
    
    def test_get_kpi_charts_endpoint(self):
        """Test KPI charts generation endpoint"""
        response = client.get("/api/visualization/kpi-charts")
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "charts" in data
            assert isinstance(data["charts"], list)
    
    def test_invalid_chart_type(self):
        """Test invalid chart type handling"""
        response = client.post(
            "/api/visualization/chart",
            json={
                "chart_type": "invalid_type",
                "data": {"x": [1], "y": [2]},
                "title": "Test"
            }
        )
        
        # Should return error or handle gracefully
        assert response.status_code in [400, 500]
