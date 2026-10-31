"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_pdf_path():
    """Path to sample PDF for testing"""
    return project_root / "data" / "sample" / "sample_business_report_2025.pdf"


@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return """
    Business Performance Report 2025
    
    Revenue Analysis:
    Total Revenue: 450 Lakhs
    Q1 Revenue: 100 Lakhs
    Q2 Revenue: 120 Lakhs
    
    Profit Margin: 25%
    Top Products: Widget A, Widget B, Widget C
    Top Regions: North, South, West
    """


@pytest.fixture
def sample_question():
    """Sample question for testing"""
    return "What was the total revenue in 2025?"


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing"""
    return "The total revenue in 2025 was 450 Lakhs."


@pytest.fixture
def sample_metadata():
    """Sample document metadata"""
    return {
        "document_id": "test_doc_123",
        "filename": "test_report.pdf",
        "page_number": 1,
        "chunk_id": "chunk_0",
        "year": 2025
    }
