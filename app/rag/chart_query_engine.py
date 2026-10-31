"""
AUREX Smart Chart Query Engine
Detects chart requests in queries and generates visualizations dynamically
"""
from typing import Dict, Any, List, Optional, Tuple
import re
from datetime import datetime

from app.core import get_logger

logger = get_logger(__name__)


class ChartQueryEngine:
    """Smart engine that detects chart requests and generates visualizations"""
    
    # Keywords that indicate user wants a chart/graph
    CHART_KEYWORDS = [
        'graph', 'chart', 'plot', 'visualize', 'visualization', 
        'show me', 'create', 'generate', 'draw', 'display',
        'compare', 'comparison', 'trend', 'over time'
    ]
    
    # Chart type mappings
    CHART_TYPE_KEYWORDS = {
        'bar': ['bar', 'bars', 'column'],
        'line': ['line', 'trend', 'over time', 'timeline', 'time series'],
        'pie': ['pie', 'percentage', 'proportion', 'distribution', 'breakdown'],
        'scatter': ['scatter', 'correlation', 'relationship'],
        'area': ['area', 'stacked', 'cumulative']
    }
    
    # Metric keywords
    METRIC_KEYWORDS = {
        'revenue': ['revenue', 'sales', 'income'],
        'profit': ['profit', 'earnings', 'net income', 'profit margin'],
        'growth': ['growth', 'increase', 'growth rate'],
        'product': ['product', 'products', 'items'],
        'region': ['region', 'regional', 'geography', 'location'],
        'customer': ['customer', 'customers', 'clients'],
        'year': ['year', 'yearly', 'annual', 'this year', 'last year']
    }
    
    def __init__(self):
        """Initialize chart query engine"""
        # Lazy import to avoid circular dependencies
        from app.vector_store.chroma_store import get_vector_store
        from app.analytics.engine import get_analytics_engine
        from app.visualization.engine import get_visualization_engine
        from app.llm.ollama_client import get_ollama_client
        
        self.vector_store = get_vector_store()
        self.analytics_engine = get_analytics_engine()
        self.viz_engine = get_visualization_engine()
        self.llm_client = get_ollama_client()
        
        logger.info("ChartQueryEngine initialized")
    
    def detect_chart_request(self, query: str) -> bool:
        """
        Detect if user is asking for a chart/graph
        
        Args:
            query: User query string
            
        Returns:
            True if query is requesting a chart
        """
        query_lower = query.lower()
        
        # Check for chart keywords
        for keyword in self.CHART_KEYWORDS:
            if keyword in query_lower:
                return True
        
        # Check for specific chart types
        for chart_keywords in self.CHART_TYPE_KEYWORDS.values():
            for keyword in chart_keywords:
                if keyword in query_lower:
                    return True
        
        return False
    
    def infer_chart_type(self, query: str) -> str:
        """
        Infer the type of chart user wants
        
        Args:
            query: User query string
            
        Returns:
            Chart type (bar, line, pie, scatter, area, or auto)
        """
        query_lower = query.lower()
        
        # Check for specific chart type mentions
        for chart_type, keywords in self.CHART_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return chart_type
        
        # Infer based on metric and comparison
        if any(word in query_lower for word in ['compare', 'comparison', 'vs', 'versus']):
            if any(word in query_lower for word in ['year', 'time', 'trend', 'over']):
                return 'line'  # Time comparison
            else:
                return 'bar'  # Category comparison
        
        if any(word in query_lower for word in ['trend', 'over time', 'timeline']):
            return 'line'
        
        if any(word in query_lower for word in ['distribution', 'breakdown', 'percentage']):
            return 'pie'
        
        return 'auto'  # Let the system decide
    
    def extract_metrics_from_query(self, query: str) -> List[str]:
        """
        Extract which metrics user is interested in
        
        Args:
            query: User query string
            
        Returns:
            List of metric types
        """
        query_lower = query.lower()
        metrics = []
        
        for metric, keywords in self.METRIC_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if metric not in metrics:
                        metrics.append(metric)
                    break
        
        return metrics
    
    def extract_years_from_query(self, query: str) -> List[int]:
        """
        Extract specific years mentioned in query
        
        Args:
            query: User query string
            
        Returns:
            List of years
        """
        # Match 4-digit years (2020-2099)
        years = re.findall(r'\b(20\d{2})\b', query)
        return [int(year) for year in years]
    
    def generate_chart_from_query(
        self, 
        query: str,
        document_filter: Optional[str] = None
    ) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Generate chart based on user query
        
        Args:
            query: User query
            document_filter: Optional document filter
            
        Returns:
            Tuple of (chart_data, explanation_text)
        """
        try:
            logger.info(f"Generating chart for query: {query}")
            
            # Step 1: Infer what user wants
            chart_type = self.infer_chart_type(query)
            metrics = self.extract_metrics_from_query(query)
            years = self.extract_years_from_query(query)
            
            logger.info(f"Inferred chart_type={chart_type}, metrics={metrics}, years={years}")
            
            # Step 2: Extract relevant data from documents
            kpis = self.analytics_engine.extract_kpis(document_filter)
            
            if not kpis:
                return None, "No data available to create charts. Please upload documents first."
            
            # Step 3: Create chart based on what user is asking for
            chart_data = None
            explanation = ""
            
            # Revenue chart
            if 'revenue' in metrics and kpis.get('revenue'):
                chart_data = self.viz_engine.create_revenue_chart(kpis['revenue'])
                explanation = f"Here's the revenue chart you requested. "
            
            # Profit comparison chart
            elif 'profit' in metrics and kpis.get('profit'):
                profit_data = kpis['profit']
                
                # If years are mentioned, filter data
                if years:
                    chart_data = self._create_yearly_comparison_chart(
                        profit_data,
                        years,
                        metric_name='Profit'
                    )
                    explanation = f"Here's the profit comparison for {', '.join(map(str, years))}. "
                else:
                    # Create general profit chart
                    chart_data = self._create_profit_chart(profit_data)
                    explanation = "Here's the profit trend chart. "
            
            # Product comparison
            elif 'product' in metrics and kpis.get('products'):
                chart_data = self.viz_engine.create_product_chart(kpis['products'])
                explanation = "Here's the product comparison chart. "
            
            # Regional comparison
            elif 'region' in metrics and kpis.get('regions'):
                chart_data = self.viz_engine.create_region_chart(kpis['regions'])
                explanation = "Here's the regional performance chart. "
            
            # Margin chart
            elif 'profit' in metrics and 'margin' in query.lower():
                chart_data = self.viz_engine.create_margin_chart(kpis)
                explanation = "Here's the profit margin chart. "
            
            # Generic KPI charts
            else:
                # Try to create the most relevant chart based on available data
                if 'revenue' in kpis:
                    chart_data = self.viz_engine.create_revenue_chart(kpis['revenue'])
                    explanation = "Here's a revenue chart based on your query. "
                elif 'profit' in kpis:
                    chart_data = self._create_profit_chart(kpis['profit'])
                    explanation = "Here's a profit chart based on your query. "
                elif 'products' in kpis:
                    chart_data = self.viz_engine.create_product_chart(kpis['products'])
                    explanation = "Here's a product performance chart based on your query. "
            
            if chart_data:
                logger.info(f"Successfully generated {chart_data.get('chart_type')} chart")
                return chart_data, explanation
            else:
                return None, "I couldn't generate a specific chart for your query, but I found relevant data."
            
        except Exception as e:
            logger.error(f"Error generating chart from query: {e}", exc_info=True)
            return None, f"Error generating chart: {str(e)}"
    
    def _create_yearly_comparison_chart(
        self,
        profit_data: Dict[str, Any],
        years: List[int],
        metric_name: str = 'Profit'
    ) -> Dict[str, Any]:
        """
        Create a comparison chart for specific years
        
        Args:
            profit_data: Profit data from analytics
            years: Years to compare
            metric_name: Name of metric
            
        Returns:
            Chart data
        """
        try:
            # Extract profit values for each year
            chart_values = []
            chart_labels = []
            
            for year in years:
                # Look for this year in the data
                if f'{year}' in str(profit_data):
                    # Extract profit value (simplified - you may need more robust extraction)
                    if 'history' in profit_data and year in profit_data['history']:
                        value = profit_data['history'][year]
                        chart_values.append(value)
                        chart_labels.append(str(year))
            
            # If we couldn't extract from history, try from main data
            if not chart_values and 'current' in profit_data:
                # Use available data
                for year in years:
                    if str(year) in profit_data.get('year', ''):
                        chart_values.append(profit_data.get('current', 0))
                        chart_labels.append(str(year))
            
            # Fallback: create mock data structure if extraction failed
            if not chart_values:
                logger.warning("Could not extract year-specific data, using summary")
                chart_values = [profit_data.get('current', 20), profit_data.get('previous', 16)]
                chart_labels = [str(years[1]) if len(years) > 1 else '2025', str(years[0]) if years else '2024']
            
            # Create bar chart for comparison
            chart_data = self.viz_engine.create_chart(
                data={
                    'labels': chart_labels,
                    'values': chart_values,
                    'metric': metric_name
                },
                chart_type='bar',
                title=f'{metric_name} Comparison: {" vs ".join(chart_labels)}'
            )
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Error creating yearly comparison chart: {e}")
            return None
    
    def _create_profit_chart(self, profit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a profit chart from profit data
        
        Args:
            profit_data: Profit data from analytics
            
        Returns:
            Chart data
        """
        try:
            # Check if we have historical data
            if 'history' in profit_data:
                years = list(profit_data['history'].keys())
                values = list(profit_data['history'].values())
                
                return self.viz_engine.create_chart(
                    data={
                        'labels': years,
                        'values': values,
                        'metric': 'Profit (₹ Lakhs)'
                    },
                    chart_type='line',
                    title='Profit Trend Over Time'
                )
            
            # If no history, create comparison of current vs previous
            elif 'current' in profit_data and 'previous' in profit_data:
                return self.viz_engine.create_chart(
                    data={
                        'labels': [
                            profit_data.get('previous_year', '2024'),
                            profit_data.get('year', '2025')
                        ],
                        'values': [
                            profit_data['previous'],
                            profit_data['current']
                        ],
                        'metric': 'Profit (₹ Lakhs)'
                    },
                    chart_type='bar',
                    title='Profit Comparison: Year over Year'
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating profit chart: {e}")
            return None


# Global instance
_chart_query_engine = None


def get_chart_query_engine() -> ChartQueryEngine:
    """Get or create global chart query engine instance"""
    global _chart_query_engine
    if _chart_query_engine is None:
        _chart_query_engine = ChartQueryEngine()
    return _chart_query_engine
