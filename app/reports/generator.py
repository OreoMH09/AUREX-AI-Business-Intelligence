"""
AUREX Report Generator
Creates professional business reports with charts and analysis
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

from app.analytics.engine import get_analytics_engine
from app.visualization.engine import get_visualization_engine
from app.rag.query_engine import get_query_engine
from app.core import settings, get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generator for business reports"""
    
    def __init__(self):
        """Initialize report generator"""
        self.analytics_engine = get_analytics_engine()
        self.viz_engine = get_visualization_engine()
        self.query_engine = get_query_engine()
        self.output_dir = Path("data/reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("ReportGenerator initialized")
    
    def generate_report(
        self,
        document_id: Optional[str] = None,
        report_type: str = 'executive',
        format: str = 'html'
    ) -> Dict[str, Any]:
        """
        Generate a business report
        
        Args:
            document_id: Optional document ID to filter
            report_type: Type of report ('executive', 'detailed', 'summary')
            format: Output format ('html', 'markdown', 'json')
            
        Returns:
            Report data with content and metadata
        """
        try:
            logger.info(f"Generating {report_type} report in {format} format")
            
            # Extract KPIs
            kpis = self.analytics_engine.extract_kpis(document_id)
            
            # Analyze trends
            trends = self.analytics_engine.analyze_trends(kpis)
            
            # Generate insights
            insights = self._generate_insights(kpis, trends)
            
            # Create visualizations
            charts = self.viz_engine.create_kpi_charts(kpis)
            
            # Build report structure
            report_data = {
                'title': self._get_report_title(report_type),
                'generated_at': datetime.utcnow().isoformat(),
                'report_type': report_type,
                'executive_summary': self._create_executive_summary(kpis, trends),
                'kpis': kpis,
                'trends': trends,
                'insights': insights,
                'charts': charts,
                'recommendations': self._generate_recommendations(kpis, trends)
            }
            
            # Format report
            if format == 'html':
                content = self._format_html(report_data)
            elif format == 'markdown':
                content = self._format_markdown(report_data)
            else:
                content = json.dumps(report_data, indent=2)
            
            # Save report
            filename = self._save_report(content, report_type, format)
            
            return {
                'success': True,
                'filename': filename,
                'report_data': report_data,
                'content': content,
                'format': format
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_executive_summary(
        self,
        kpis: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> str:
        """Create executive summary"""
        try:
            summary_parts = []
            
            # Revenue summary
            if 'revenue' in kpis and kpis['revenue']:
                revenue = kpis['revenue']
                summary_parts.append(
                    f"Total revenue reached ₹{revenue.get('value', 0)} lakhs"
                    f"{' in ' + str(revenue.get('year', '')) if revenue.get('year') else ''}."
                )
            
            # Profit margin
            if 'margin' in kpis and kpis['margin']:
                margin = kpis['margin']
                summary_parts.append(
                    f"Profit margin stood at {margin.get('value', 0)}%."
                )
            
            # Top product
            if 'top_product' in trends and trends['top_product']:
                top_prod = trends['top_product']
                summary_parts.append(
                    f"{top_prod.get('name', 'Top product')} led with ₹{top_prod.get('sales', 0)} lakhs in sales."
                )
            
            # Top region
            if 'top_region' in trends and trends['top_region']:
                top_region = trends['top_region']
                summary_parts.append(
                    f"{top_region.get('name', 'Top region')} was the best performing region with ₹{top_region.get('sales', 0)} lakhs."
                )
            
            return " ".join(summary_parts) if summary_parts else "Business performance summary not available."
            
        except Exception as e:
            logger.error(f"Error creating executive summary: {e}")
            return "Executive summary could not be generated."
    
    def _generate_insights(
        self,
        kpis: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> List[str]:
        """Generate key insights from data"""
        insights = []
        
        try:
            # Product insights
            if 'products' in kpis and kpis['products']:
                products = kpis['products']
                if len(products) > 1:
                    sorted_products = sorted(products, key=lambda x: x.get('sales', 0), reverse=True)
                    top = sorted_products[0]
                    bottom = sorted_products[-1]
                    
                    insights.append(
                        f"Product performance shows significant variation, with {top.get('name')} "
                        f"outperforming {bottom.get('name')} by "
                        f"{top.get('sales', 0) - bottom.get('sales', 0):.1f} lakhs."
                    )
            
            # Regional insights
            if 'regions' in kpis and kpis['regions']:
                regions = kpis['regions']
                if len(regions) > 1:
                    total_sales = sum(r.get('sales', 0) for r in regions)
                    top_region = max(regions, key=lambda x: x.get('sales', 0))
                    contribution = (top_region.get('sales', 0) / total_sales * 100) if total_sales > 0 else 0
                    
                    insights.append(
                        f"{top_region.get('name')} contributes {contribution:.1f}% of total regional sales."
                    )
            
            # Profitability insight
            if 'margin' in kpis and kpis['margin']:
                margin_value = kpis['margin'].get('value', 0)
                if margin_value > 20:
                    insights.append("Strong profit margins indicate healthy operational efficiency.")
                elif margin_value < 15:
                    insights.append("Profit margins below industry average suggest need for cost optimization.")
            
            return insights if insights else ["Detailed insights require more data points."]
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return ["Insights could not be generated."]
    
    def _generate_recommendations(
        self,
        kpis: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        try:
            # Product recommendations
            if 'top_product' in trends and 'bottom_product' in trends:
                top = trends['top_product']
                bottom = trends['bottom_product']
                
                recommendations.append(
                    f"Consider increasing investment in {top.get('name')} given its strong performance."
                )
                
                recommendations.append(
                    f"Investigate causes of underperformance in {bottom.get('name')} and develop improvement strategy."
                )
            
            # Regional recommendations
            if 'top_region' in trends:
                top_region = trends['top_region']
                recommendations.append(
                    f"Expand operations in {top_region.get('name')} to capitalize on strong market demand."
                )
            
            if 'bottom_region' in trends:
                bottom_region = trends['bottom_region']
                recommendations.append(
                    f"Develop targeted interventions for {bottom_region.get('name')} to reverse negative trends."
                )
            
            # General recommendation
            recommendations.append(
                "Maintain focus on operational efficiency to sustain profit margins."
            )
            
            return recommendations if recommendations else ["Recommendations require more comprehensive data analysis."]
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Recommendations could not be generated."]
    
    def _format_html(self, report_data: Dict[str, Any]) -> str:
        """Format report as HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{report_data['title']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #1f77b4;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2c5282;
            margin-top: 30px;
        }}
        .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
        .summary {{
            background: #f0f4f8;
            padding: 20px;
            border-left: 4px solid #1f77b4;
            margin: 20px 0;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .kpi-card {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .kpi-value {{
            font-size: 2em;
            font-weight: bold;
            color: #1f77b4;
        }}
        .kpi-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .insight {{
            background: #fff3cd;
            padding: 10px 15px;
            margin: 10px 0;
            border-left: 3px solid #ffc107;
        }}
        .recommendation {{
            background: #d4edda;
            padding: 10px 15px;
            margin: 10px 0;
            border-left: 3px solid #28a745;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <h1>{report_data['title']}</h1>
    <div class="meta">
        Generated on {datetime.fromisoformat(report_data['generated_at']).strftime('%B %d, %Y at %I:%M %p')}
    </div>
    
    <h2>Executive Summary</h2>
    <div class="summary">
        {report_data['executive_summary']}
    </div>
    
    <h2>Key Performance Indicators</h2>
    <div class="kpi-grid">
"""
        
        # Add KPI cards
        kpis = report_data['kpis']
        if 'revenue' in kpis and kpis['revenue']:
            revenue = kpis['revenue']
            html += f"""
        <div class="kpi-card">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-value">₹{revenue.get('value', 0)}</div>
            <div class="kpi-label">Lakhs</div>
        </div>
"""
        
        if 'profit' in kpis and kpis['profit']:
            profit = kpis['profit']
            html += f"""
        <div class="kpi-card">
            <div class="kpi-label">Profit</div>
            <div class="kpi-value">₹{profit.get('value', 0)}</div>
            <div class="kpi-label">Lakhs</div>
        </div>
"""
        
        if 'margin' in kpis and kpis['margin']:
            margin = kpis['margin']
            html += f"""
        <div class="kpi-card">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-value">{margin.get('value', 0)}%</div>
        </div>
"""
        
        html += """
    </div>
    
    <h2>Key Insights</h2>
"""
        
        for insight in report_data['insights']:
            html += f'<div class="insight">💡 {insight}</div>\n'
        
        html += """
    <h2>Recommendations</h2>
"""
        
        for rec in report_data['recommendations']:
            html += f'<div class="recommendation">✅ {rec}</div>\n'
        
        html += """
</body>
</html>
"""
        
        return html
    
    def _format_markdown(self, report_data: Dict[str, Any]) -> str:
        """Format report as Markdown"""
        md = f"""# {report_data['title']}

**Generated:** {datetime.fromisoformat(report_data['generated_at']).strftime('%B %d, %Y at %I:%M %p')}

---

## Executive Summary

{report_data['executive_summary']}

---

## Key Performance Indicators

"""
        
        kpis = report_data['kpis']
        if 'revenue' in kpis and kpis['revenue']:
            md += f"**Revenue:** ₹{kpis['revenue'].get('value', 0)} Lakhs\n\n"
        
        if 'profit' in kpis and kpis['profit']:
            md += f"**Profit:** ₹{kpis['profit'].get('value', 0)} Lakhs\n\n"
        
        if 'margin' in kpis and kpis['margin']:
            md += f"**Profit Margin:** {kpis['margin'].get('value', 0)}%\n\n"
        
        md += "---\n\n## Key Insights\n\n"
        
        for insight in report_data['insights']:
            md += f"💡 {insight}\n\n"
        
        md += "---\n\n## Recommendations\n\n"
        
        for rec in report_data['recommendations']:
            md += f"✅ {rec}\n\n"
        
        return md
    
    def _save_report(self, content: str, report_type: str, format: str) -> str:
        """Save report to file"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type}_report_{timestamp}.{format}"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Report saved: {filename}")
        return filename
    
    def _get_report_title(self, report_type: str) -> str:
        """Get report title based on type"""
        titles = {
            'executive': 'Executive Business Report',
            'detailed': 'Detailed Analysis Report',
            'summary': 'Business Summary Report'
        }
        return titles.get(report_type, 'Business Report')


# Global report generator instance
report_generator = None


def get_report_generator() -> ReportGenerator:
    """Get or create global report generator instance"""
    global report_generator
    if report_generator is None:
        report_generator = ReportGenerator()
    return report_generator
