"""
End-to-end tests for complete RAG pipeline
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import time


client = TestClient(app)


@pytest.mark.e2e
@pytest.mark.slow
class TestRAGPipeline:
    """Test suite for end-to-end RAG workflows"""
    
    def test_complete_query_workflow(self):
        """Test complete query workflow from start to finish"""
        # Step 1: Check system health
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
        
        # Step 2: Check if documents exist
        docs_response = client.get("/api/documents")
        assert docs_response.status_code == 200
        
        docs_data = docs_response.json()
        
        if docs_data.get("total", 0) == 0:
            pytest.skip("No documents available for testing")
        
        # Step 3: Perform a query
        query_response = client.post(
            "/api/query",
            json={"question": "What is the total revenue?"}
        )
        
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        assert "answer" in query_data
        assert "sources" in query_data
        assert "processing_time_ms" in query_data
        
        # Verify answer is not empty
        assert len(query_data["answer"]) > 0
        
        # Step 4: Check evaluation metrics were recorded
        time.sleep(1)  # Give time for evaluation to process
        
        eval_response = client.get("/api/evaluation/metrics")
        assert eval_response.status_code == 200
        
        eval_data = eval_response.json()
        assert eval_data["success"] is True
    
    def test_analytics_to_visualization_workflow(self):
        """Test workflow from analytics to visualization"""
        # Step 1: Get KPIs
        kpis_response = client.get("/api/analytics/kpis")
        
        if kpis_response.status_code == 404:
            pytest.skip("No data available for analytics")
        
        assert kpis_response.status_code == 200
        kpis_data = kpis_response.json()
        
        assert "kpis" in kpis_data
        
        # Step 2: Generate charts from KPIs
        charts_response = client.get("/api/visualization/kpi-charts")
        
        assert charts_response.status_code == 200
        charts_data = charts_response.json()
        
        assert "charts" in charts_data
        assert len(charts_data["charts"]) > 0
    
    def test_report_generation_workflow(self):
        """Test complete report generation workflow"""
        # Generate a report
        report_response = client.post(
            "/api/reports/generate",
            json={
                "report_type": "executive",
                "format": "json"
            }
        )
        
        if report_response.status_code == 404:
            pytest.skip("No data available for report generation")
        
        assert report_response.status_code == 200
        report_data = report_response.json()
        
        assert report_data["success"] is True
        assert "filename" in report_data
        assert "report_data" in report_data
        
        # Verify report structure
        report_content = report_data["report_data"]
        assert "executive_summary" in report_content or "kpis" in report_content
