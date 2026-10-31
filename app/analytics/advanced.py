"""
AUREX Advanced Analytics
Period comparison, trend analysis, and what-if scenarios
"""
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

from app.rag.query_engine import get_query_engine
from app.core import get_logger

logger = get_logger(__name__)


class AdvancedAnalytics:
    """Advanced analytics for comparison and scenario analysis"""
    
    def __init__(self):
        """Initialize advanced analytics"""
        self.query_engine = get_query_engine()
        logger.info("AdvancedAnalytics initialized")
    
    def compare_periods(
        self,
        period1: str,
        period2: str,
        metric: str = 'revenue',
        document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare metrics between two time periods
        
        Args:
            period1: First period (e.g., "2024", "Q1 2025")
            period2: Second period
            metric: Metric to compare
            document_id: Optional document filter
            
        Returns:
            Comparison results with change calculations
        """
        try:
            logger.info(f"Comparing {metric} between {period1} and {period2}")
            
            # Query for period 1
            query1 = f"What was the {metric} in {period1}? Provide exact number."
            result1 = self.query_engine.query(query1, document_filter=document_id)
            value1 = self._extract_first_number(result1.get('answer', ''))
            
            # Query for period 2
            query2 = f"What was the {metric} in {period2}? Provide exact number."
            result2 = self.query_engine.query(query2, document_filter=document_id)
            value2 = self._extract_first_number(result2.get('answer', ''))
            
            comparison = {
                'period1': {
                    'label': period1,
                    'value': value1,
                    'answer': result1.get('answer', '')
                },
                'period2': {
                    'label': period2,
                    'value': value2,
                    'answer': result2.get('answer', '')
                },
                'metric': metric
            }
            
            # Calculate changes if both values exist
            if value1 is not None and value2 is not None:
                absolute_change = value2 - value1
                percentage_change = (absolute_change / value1 * 100) if value1 != 0 else 0
                
                comparison['change'] = {
                    'absolute': absolute_change,
                    'percentage': percentage_change,
                    'direction': 'increase' if absolute_change > 0 else 'decrease' if absolute_change < 0 else 'unchanged',
                    'interpretation': self._interpret_change(absolute_change, percentage_change, metric)
                }
            else:
                comparison['change'] = None
                comparison['note'] = 'Insufficient data for comparison'
            
            comparison['compared_at'] = datetime.utcnow().isoformat()
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing periods: {e}", exc_info=True)
            return {
                'error': str(e),
                'period1': {'label': period1, 'value': None},
                'period2': {'label': period2, 'value': None}
            }
    
    def year_over_year(
        self,
        base_year: int,
        metric: str = 'revenue',
        document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Year-over-year comparison
        
        Args:
            base_year: Base year for comparison
            metric: Metric to analyze
            document_id: Optional document filter
            
        Returns:
            YoY analysis
        """
        try:
            logger.info(f"Year-over-year analysis for {metric} (base: {base_year})")
            
            current_year = base_year
            previous_year = base_year - 1
            
            comparison = self.compare_periods(
                period1=str(previous_year),
                period2=str(current_year),
                metric=metric,
                document_id=document_id
            )
            
            comparison['analysis_type'] = 'year_over_year'
            comparison['base_year'] = base_year
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error in YoY analysis: {e}")
            return {'error': str(e)}
    
    def scenario_analysis(
        self,
        baseline: Dict[str, float],
        scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        What-if scenario analysis
        
        Args:
            baseline: Baseline metrics (e.g., {'revenue': 94, 'costs': 73.32})
            scenarios: List of scenarios with changes
                Example: [{'name': 'Cost Reduction', 'costs': -10}]
            
        Returns:
            Scenario analysis with projections
        """
        try:
            logger.info(f"Running scenario analysis with {len(scenarios)} scenarios")
            
            results = {
                'baseline': baseline.copy(),
                'scenarios': []
            }
            
            # Calculate baseline profit if not provided
            if 'profit' not in baseline and 'revenue' in baseline and 'costs' in baseline:
                baseline['profit'] = baseline['revenue'] - baseline['costs']
                baseline['margin'] = (baseline['profit'] / baseline['revenue'] * 100) if baseline['revenue'] > 0 else 0
            
            # Analyze each scenario
            for scenario in scenarios:
                scenario_result = self._calculate_scenario(baseline, scenario)
                results['scenarios'].append(scenario_result)
            
            # Find best and worst scenarios
            if results['scenarios']:
                results['best_scenario'] = max(
                    results['scenarios'],
                    key=lambda x: x.get('projected', {}).get('profit', 0)
                )
                results['worst_scenario'] = min(
                    results['scenarios'],
                    key=lambda x: x.get('projected', {}).get('profit', 0)
                )
            
            results['analyzed_at'] = datetime.utcnow().isoformat()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in scenario analysis: {e}", exc_info=True)
            return {'error': str(e), 'baseline': baseline}
    
    def trend_projection(
        self,
        historical_data: List[Dict[str, Any]],
        periods_ahead: int = 3
    ) -> Dict[str, Any]:
        """
        Project future trends based on historical data
        
        Args:
            historical_data: List of historical data points
                Example: [{'period': '2023', 'value': 75}, {'period': '2024', 'value': 80}]
            periods_ahead: Number of periods to project
            
        Returns:
            Trend projection
        """
        try:
            logger.info(f"Projecting {periods_ahead} periods ahead")
            
            if len(historical_data) < 2:
                return {'error': 'Insufficient historical data for projection'}
            
            # Calculate average growth rate
            values = [d['value'] for d in historical_data]
            growth_rates = []
            
            for i in range(1, len(values)):
                if values[i-1] != 0:
                    growth_rate = (values[i] - values[i-1]) / values[i-1]
                    growth_rates.append(growth_rate)
            
            avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0
            
            # Project future periods
            last_value = values[-1]
            projections = []
            
            for i in range(1, periods_ahead + 1):
                projected_value = last_value * ((1 + avg_growth_rate) ** i)
                projections.append({
                    'period_offset': i,
                    'projected_value': projected_value,
                    'confidence': 'medium' if i <= 2 else 'low'
                })
            
            return {
                'historical_data': historical_data,
                'average_growth_rate': avg_growth_rate * 100,  # As percentage
                'projections': projections,
                'method': 'average_growth_rate',
                'projected_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in trend projection: {e}")
            return {'error': str(e)}
    
    def _calculate_scenario(
        self,
        baseline: Dict[str, float],
        scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate projections for a scenario"""
        projected = baseline.copy()
        changes = {}
        
        scenario_name = scenario.get('name', 'Unnamed Scenario')
        
        # Apply changes
        for key, change in scenario.items():
            if key == 'name':
                continue
            
            if key in projected:
                if isinstance(change, str) and change.endswith('%'):
                    # Percentage change
                    pct = float(change.rstrip('%'))
                    old_value = projected[key]
                    new_value = old_value * (1 + pct / 100)
                    projected[key] = new_value
                    changes[key] = {'old': old_value, 'new': new_value, 'change': new_value - old_value}
                else:
                    # Absolute change
                    old_value = projected[key]
                    new_value = old_value + float(change)
                    projected[key] = new_value
                    changes[key] = {'old': old_value, 'new': new_value, 'change': change}
        
        # Recalculate profit and margin
        if 'revenue' in projected and 'costs' in projected:
            projected['profit'] = projected['revenue'] - projected['costs']
            projected['margin'] = (projected['profit'] / projected['revenue'] * 100) if projected['revenue'] > 0 else 0
        
        return {
            'name': scenario_name,
            'projected': projected,
            'changes': changes,
            'impact': self._assess_scenario_impact(baseline, projected)
        }
    
    def _assess_scenario_impact(
        self,
        baseline: Dict[str, float],
        projected: Dict[str, float]
    ) -> str:
        """Assess the impact of a scenario"""
        if 'profit' in baseline and 'profit' in projected:
            profit_change = projected['profit'] - baseline['profit']
            
            if profit_change > 0:
                return f"Positive impact: Profit increases by ₹{profit_change:.2f} lakhs"
            elif profit_change < 0:
                return f"Negative impact: Profit decreases by ₹{abs(profit_change):.2f} lakhs"
            else:
                return "Neutral impact: No change in profit"
        
        return "Impact assessment not available"
    
    def _interpret_change(
        self,
        absolute: float,
        percentage: float,
        metric: str
    ) -> str:
        """Interpret the meaning of a change"""
        direction = "increased" if absolute > 0 else "decreased" if absolute < 0 else "remained stable"
        
        if abs(percentage) < 1:
            magnitude = "marginally"
        elif abs(percentage) < 10:
            magnitude = "moderately"
        else:
            magnitude = "significantly"
        
        return f"{metric.capitalize()} {magnitude} {direction} by {abs(percentage):.1f}%"
    
    def _extract_first_number(self, text: str) -> Optional[float]:
        """Extract first number from text"""
        if not text:
            return None
        
        # Pattern for numbers including decimals
        pattern = r'(\d+(?:,\d+)*(?:\.\d+)?)'
        matches = re.findall(pattern, text)
        
        if matches:
            try:
                # Remove commas and convert
                return float(matches[0].replace(',', ''))
            except:
                pass
        
        return None


# Global advanced analytics instance
advanced_analytics = None


def get_advanced_analytics() -> AdvancedAnalytics:
    """Get or create global advanced analytics instance"""
    global advanced_analytics
    if advanced_analytics is None:
        advanced_analytics = AdvancedAnalytics()
    return advanced_analytics
