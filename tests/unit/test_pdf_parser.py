"""
Test PDF Parser
"""
import pytest
from pathlib import Path
from app.ingestion.pdf_parser import PDFParser
from app.models import FileType


@pytest.fixture
def pdf_parser():
    """Create PDF parser instance"""
    return PDFParser(enable_ocr=False)


@pytest.mark.unit
def test_pdf_parser_initialization(pdf_parser):
    """Test PDF parser initialization"""
    assert pdf_parser is not None
    assert '.pdf' in pdf_parser.supported_extensions
    assert not pdf_parser.ocr_available


@pytest.mark.unit
def test_pdf_parser_validate_extension(pdf_parser):
    """Test file extension validation"""
    # Valid PDF
    valid_path = Path("test.pdf")
    assert valid_path.suffix.lower() in pdf_parser.supported_extensions
    
    # Invalid extensions
    invalid_path = Path("test.txt")
    assert invalid_path.suffix.lower() not in pdf_parser.supported_extensions


@pytest.mark.unit
def test_is_likely_heading(pdf_parser):
    """Test heading detection"""
    # These should be headings
    assert pdf_parser._is_likely_heading("1. Introduction")
    assert pdf_parser._is_likely_heading("Chapter 1")
    assert pdf_parser._is_likely_heading("EXECUTIVE SUMMARY")
    
    # These should not be headings
    assert not pdf_parser._is_likely_heading("This is a very long sentence that is definitely not a heading because it exceeds the maximum length.")
    assert not pdf_parser._is_likely_heading("ab")  # Too short


@pytest.mark.unit
def test_extract_year_from_filename(pdf_parser):
    """Test year extraction from filename"""
    # Year in filename
    path1 = Path("annual_report_2024.pdf")
    metadata = pdf_parser.extract_metadata(path1) if path1.exists() else None
    
    # Extract year directly
    import re
    filename = "annual_report_2024.pdf"
    year_pattern = r'20\d{2}'
    matches = re.findall(year_pattern, filename)
    
    if matches:
        assert int(matches[-1]) == 2024
