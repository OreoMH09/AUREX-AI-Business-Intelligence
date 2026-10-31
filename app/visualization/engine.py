"""
AUREX Visualization Engine
Automated chart generation with Plotly
"""
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from app.core import get_logger

logger = get_logger(__name__)


class VisualizationEngine:
    """Engine for automated data visualization"""
    
    def __init__(self):
        """Initialize visualization engine"""
        self.chart_types = [
            'bar', 'line', 'pie', 'scatter', 
            'area', 'histogram', 'box'
        ]
        logger.info("VisualizationEngine initialized")
    
    def create_chart(
        self,
        data: Dict[str, Any],
        chart_type: str = 'auto',
        title: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a chart from data
        
        Args:
            data: Data dictionary with labels and values
            chart_type: Type of chart ('auto' for automatic selection)
            title: Chart title
            **kwargs: Additional chart options
            
        Returns:
            Plotly chart as JSON
        """
        try:
            logger.info(f"Creating {chart_type} chart")
            
            # Auto-select chart type if needed
            if chart_type == 'auto':
                chart_type = self._select_chart_type(data)
            
            # Create appropriate chart
            if chart_type == 'bar':
                fig = self._create_bar_chart(data, title, **kwargs)
            elif chart_type == 'line':
                fig = self._create_line_chart(data, title, **kwargs)
            elif chart_type == 'pie':
                fig = self._create_pie_chart(data, title, **kwargs)
            elif chart_type == 'scatter':
                fig = self._create_scatter_chart(data, title, **kwargs)
            elif chart_type == 'area':
                fig = self._create_area_chart(data, title, **kwargs)
            else:
                fig = self._create_bar_chart(data, title, **kwargs)
            
            # Convert to JSON
            chart_json = fig.to_json()
            
            return {
                'chart': chart_json,
                'chart_type': chart_type,
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating chart: {e}", exc_info=True)
            return {}
    
    def create_kpi_charts(self, kpis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create multiple charts from KPI data
        
        Args:
            kpis: KPI dictionary
            
        Returns:
            List of chart dictionaries
        """
        try:
            charts = []
            
            # Revenue chart
            if 'revenue' in kpis and kpis['revenue']:
                revenue_chart = self.create_revenue_chart(kpis['revenue'])
                if revenue_chart:
                    charts.append(revenue_chart)
            
            # Product performance chart
            if 'products' in kpis and kpis['products']:
                product_chart = self.create_product_chart(kpis['products'])
                if product_chart:
                    charts.append(product_chart)
            
            # Regional performance chart
            if 'regions' in kpis and kpis['regions']:
                region_chart = self.create_region_chart(kpis['regions'])
                if region_chart:
                    charts.append(region_chart)
            
            # Profit margin chart
            if 'margin' in kpis and kpis['margin']:
                margin_chart = self.create_margin_chart(kpis)
                if margin_chart:
                    charts.append(margin_chart)
            
            return charts
            
        except Exception as e:
            logger.error(f"Error creating KPI charts: {e}", exc_info=True)
            return []
    
    def create_revenue_chart(self, revenue_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create revenue visualization"""
        try:
            value = revenue_data.get('value', 0)
            year = revenue_data.get('year', 'Current')
            
            fig = go.Figure(go.Indicator(
                mode="number+delta",
                value=value,
                title={'text': f"Revenue ({year})"},
                number={'prefix': "₹", 'suffix': " Lakhs"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            
            fig.update_layout(
                height=250,
                margin=dict(t=50, b=30, l=30, r=30)
            )
            
            return {
                'chart': fig.to_json(),
                'chart_type': 'indicator',
                'title': 'Revenue',
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating revenue chart: {e}")
            return None
    
    def create_product_chart(self, products: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create product performance chart"""
        try:
            names = [p.get('name', f'Product {i+1}') for i, p in enumerate(products)]
            sales = [p.get('sales', 0) for p in products]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=names,
                    y=sales,
                    marker_color='lightblue',
                    text=sales,
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title='Product Performance',
                xaxis_title='Products',
                yaxis_title='Sales (Lakhs)',
                height=400,
                showlegend=False
            )
            
            return {
                'chart': fig.to_json(),
                'chart_type': 'bar',
                'title': 'Product Performance',
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating product chart: {e}")
            return None
    
    def create_region_chart(self, regions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create regional performance chart"""
        try:
            names = [r.get('name', f'Region {i+1}') for i, r in enumerate(regions)]
            sales = [r.get('sales', 0) for r in regions]
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=names,
                    values=sales,
                    hole=0.3,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Set3)
                )
            ])
            
            fig.update_layout(
                title='Regional Sales Distribution',
                height=400
            )
            
            return {
                'chart': fig.to_json(),
                'chart_type': 'pie',
                'title': 'Regional Distribution',
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating region chart: {e}")
            return None
    
    def create_margin_chart(self, kpis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create profit margin visualization"""
        try:
            margin = kpis.get('margin', {})
            margin_value = margin.get('value', 0)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=margin_value,
                title={'text': "Profit Margin"},
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 10], 'color': "lightgray"},
                        {'range': [10, 20], 'color': "lightyellow"},
                        {'range': [20, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 15
                    }
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=50, b=30, l=30, r=30)
            )
            
            return {
                'chart': fig.to_json(),
                'chart_type': 'gauge',
                'title': 'Profit Margin',
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating margin chart: {e}")
            return None
    
    def _create_bar_chart(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create bar chart"""
        labels = data.get('labels', [])
        values = data.get('values', [])
        
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=kwargs.get('color', 'lightblue'),
                text=values,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=title or 'Bar Chart',
            xaxis_title=kwargs.get('x_label', 'Categories'),
            yaxis_title=kwargs.get('y_label', 'Values'),
            height=kwargs.get('height', 400)
        )
        
        return fig
    
    def _create_line_chart(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create line chart"""
        labels = data.get('labels', [])
        values = data.get('values', [])
        
        fig = go.Figure(data=[
            go.Scatter(
                x=labels,
                y=values,
                mode='lines+markers',
                line=dict(color=kwargs.get('color', 'blue'), width=2),
                marker=dict(size=8)
            )
        ])
        
        fig.update_layout(
            title=title or 'Line Chart',
            xaxis_title=kwargs.get('x_label', 'Time'),
            yaxis_title=kwargs.get('y_label', 'Values'),
            height=kwargs.get('height', 400)
        )
        
        return fig
    
    def _create_pie_chart(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create pie chart"""
        labels = data.get('labels', [])
        values = data.get('values', [])
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=kwargs.get('hole', 0),
                textinfo='label+percent'
            )
        ])
        
        fig.update_layout(
            title=title or 'Pie Chart',
            height=kwargs.get('height', 400)
        )
        
        return fig
    
    def _create_scatter_chart(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create scatter chart"""
        x_values = data.get('x', [])
        y_values = data.get('y', [])
        
        fig = go.Figure(data=[
            go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker=dict(
                    size=kwargs.get('marker_size', 10),
                    color=kwargs.get('color', 'blue')
                )
            )
        ])
        
        fig.update_layout(
            title=title or 'Scatter Chart',
            xaxis_title=kwargs.get('x_label', 'X'),
            yaxis_title=kwargs.get('y_label', 'Y'),
            height=kwargs.get('height', 400)
        )
        
        return fig
    
    def _create_area_chart(
        self,
        data: Dict[str, Any],
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """Create area chart"""
        labels = data.get('labels', [])
        values = data.get('values', [])
        
        fig = go.Figure(data=[
            go.Scatter(
                x=labels,
                y=values,
                fill='tozeroy',
                mode='lines',
                line=dict(color=kwargs.get('color', 'lightblue'))
            )
        ])
        
        fig.update_layout(
            title=title or 'Area Chart',
            xaxis_title=kwargs.get('x_label', 'Time'),
            yaxis_title=kwargs.get('y_label', 'Values'),
            height=kwargs.get('height', 400)
        )
        
        return fig
    
    def _select_chart_type(self, data: Dict[str, Any]) -> str:
        """Automatically select appropriate chart type"""
        # Simple logic for chart selection
        if 'labels' in data and 'values' in data:
            num_items = len(data.get('labels', []))
            
            # Pie chart for small categorical data
            if num_items <= 6:
                return 'pie'
            # Bar chart for categorical comparison
            else:
                return 'bar'
        
        # Default to bar
        return 'bar'


# Global visualization engine instance
visualization_engine = None


def get_visualization_engine() -> VisualizationEngine:
    """Get or create global visualization engine instance"""
    global visualization_engine
    if visualization_engine is None:
        visualization_engine = VisualizationEngine()
    return visualization_engine
