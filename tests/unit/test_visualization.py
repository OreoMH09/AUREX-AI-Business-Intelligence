"""
Unit tests for Visualization Engine
"""
import pytest
import json
from app.visualization.engine import VisualizationEngine


@pytest.mark.unit
class TestVisualizationEngine:
    """Test suite for VisualizationEngine"""
    
    def test_create_bar_chart(self):
        """Test bar chart creation"""
        engine = VisualizationEngine()
        
        data = {
            'x': ['Product A', 'Product B', 'Product C'],
            'y': [100, 150, 120]
        }
        
        result = engine.create_chart(
            chart_type='bar',
            data=data,
            title='Product Sales'
        )
        
        assert result is not None
        assert 'chart' in result
        assert result['title'] == 'Product Sales'
        
        # Verify it's valid JSON
        chart_json = json.loads(result['chart'])
        assert 'data' in chart_json
    
    def test_create_line_chart(self):
        """Test line chart creation"""
        engine = VisualizationEngine()
        
        data = {
            'x': ['Q1', 'Q2', 'Q3', 'Q4'],
            'y': [100, 120, 150, 180]
        }
        
        result = engine.create_chart(
            chart_type='line',
            data=data,
            title='Quarterly Growth'
        )
        
        assert result is not None
        assert result['chart_type'] == 'line'
    
    def test_create_pie_chart(self):
        """Test pie chart creation"""
        engine = VisualizationEngine()
        
        data = {
            'labels': ['North', 'South', 'East', 'West'],
            'values': [120, 150, 100, 130]
        }
        
        result = engine.create_chart(
            chart_type='pie',
            data=data,
            title='Regional Distribution'
        )
        
        assert result is not None
        assert result['chart_type'] == 'pie'
    
    def test_create_gauge_chart(self):
        """Test gauge chart creation"""
        engine = VisualizationEngine()
        
        result = engine.create_gauge_chart(
            value=75,
            title='Performance Score',
            max_value=100
        )
        
        assert result is not None
        assert 'chart' in result
    
    def test_create_indicator_chart(self):
        """Test indicator chart creation"""
        engine = VisualizationEngine()
        
        result = engine.create_indicator_chart(
            value=450,
            title='Total Revenue',
            suffix=' L'
        )
        
        assert result is not None
        assert result['chart_type'] == 'indicator'
    
    def test_invalid_chart_type(self):
        """Test handling of invalid chart type"""
        engine = VisualizationEngine()
        
        data = {'x': [1, 2], 'y': [3, 4]}
        result = engine.create_chart('invalid_type', data, 'Test')
        
        # Should handle gracefully or raise appropriate error
        assert result is None or 'error' in result
