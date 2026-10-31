"""
Integration tests for Analytics API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.integration
class TestAnalyticsAPI:
    """Test suite for analytics endpoints"""
    
    def test_get_kpis_endpoint(self):
        """Test KPI extraction endpoint"""
        response = client.get("/api/analytics/kpis")
        
        assert response.status_code in [200, 404]  # 404 if no documents
        
        if response.status_code == 200:
            data = response.json()
            assert "kpis" in data
    
    def test_get_summary_endpoint(self):
        """Test summary statistics endpoint"""
        response = client.get("/api/analytics/summary")
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "summary" in data
    
    def test_get_trends_endpoint(self):
        """Test trends analysis endpoint"""
        response = client.get("/api/analytics/trends")
        
        assert response.status_code in [200, 404]
    
    def test_period_comparison_endpoint(self):
        """Test period comparison endpoint"""
        response = client.post(
            "/api/analytics/compare",
            json={
                "period1": "2024",
                "period2": "2025",
                "metric": "revenue"
            }
        )
        
        assert response.status_code in [200, 400, 404]
    
    def test_scenario_analysis_endpoint(self):
        """Test scenario analysis endpoint"""
        response = client.post(
            "/api/analytics/scenario",
            json={
                "base_metric": "revenue",
                "change_percentage": 10
            }
        )
        
        assert response.status_code in [200, 400, 404]
