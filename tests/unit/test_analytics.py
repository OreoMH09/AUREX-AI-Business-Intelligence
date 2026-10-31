"""
Unit tests for Analytics Engine
"""
import pytest
from app.analytics.engine import AnalyticsEngine


@pytest.mark.unit
class TestAnalyticsEngine:
    """Test suite for AnalyticsEngine"""
    
    def test_extract_revenue(self):
        """Test revenue extraction from text"""
        engine = AnalyticsEngine()
        
        text = "The total revenue for 2025 was 450 Lakhs."
        result = engine._extract_revenue(text)
        
        assert result is not None
        assert result['value'] == 450
        assert '2025' in result.get('year', '')
    
    def test_extract_profit(self):
        """Test profit extraction"""
        engine = AnalyticsEngine()
        
        text = "Profit: 112.5 Lakhs"
        result = engine._extract_profit(text)
        
        assert result is not None
        assert result['value'] == 112.5
    
    def test_extract_margin(self):
        """Test profit margin extraction"""
        engine = AnalyticsEngine()
        
        text = "Profit margin is 25%"
        result = engine._extract_margin(text)
        
        assert result is not None
        assert result['value'] == 25
    
    def test_extract_products(self):
        """Test product extraction"""
        engine = AnalyticsEngine()
        
        text = "Top products are Widget A, Widget B, and Widget C"
        result = engine._extract_products(text)
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_extract_regions(self):
        """Test region extraction"""
        engine = AnalyticsEngine()
        
        text = "Regional performance: North, South, and West regions"
        result = engine._extract_regions(text)
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_parse_number(self):
        """Test number parsing utility"""
        engine = AnalyticsEngine()
        
        assert engine._parse_number("450") == 450
        assert engine._parse_number("112.5") == 112.5
        assert engine._parse_number("25%") == 25
        assert engine._parse_number("invalid") is None
