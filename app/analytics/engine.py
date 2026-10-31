"""
AUREX Analytics Engine
Automated KPI extraction and calculations from documents
"""
from typing import Dict, List, Any, Optional
import re
import pandas as pd
from datetime import datetime

from app.rag.query_engine import get_query_engine
from app.core import settings, get_logger

logger = get_logger(__name__)


class AnalyticsEngine:
    """Engine for automated business analytics"""
    
    def __init__(self):
        """Initialize analytics engine"""
        self.query_engine = get_query_engine()
        logger.info("AnalyticsEngine initialized")
    
    def extract_kpis(self, document_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract key performance indicators from documents
        
        Args:
            document_id: Optional document ID to analyze (None for all)
            
        Returns:
            Dictionary with extracted KPIs
        """
        try:
            logger.info(f"Extracting KPIs from documents using LLM")
            
            kpis = {}
            
            # Financial metrics - Now fast with Gemini!
            revenue_data = self._extract_revenue(document_id)
            if revenue_data:
                kpis['revenue'] = revenue_data
            
            profit_data = self._extract_profit(document_id)
            if profit_data:
                kpis['profit'] = profit_data
            
            margin_data = self._extract_margin(document_id)
            if margin_data:
                kpis['margin'] = margin_data
            
            growth_data = self._calculate_growth_rates(kpis)
            if growth_data:
                kpis['growth'] = growth_data
            
            # Product metrics
            product_data = self._extract_product_metrics(document_id)
            if product_data:
                kpis['products'] = product_data
            
            # Regional metrics
            regional_data = self._extract_regional_metrics(document_id)
            if regional_data:
                kpis['regions'] = regional_data
            
            kpis['extracted_at'] = datetime.utcnow().isoformat()
            kpis['document_id'] = document_id
            
            logger.info(f"Extracted {len(kpis)} KPI categories")
            return kpis
            
        except Exception as e:
            logger.error(f"Error extracting KPIs: {e}", exc_info=True)
            return {}
    
    def _extract_revenue(self, document_id: Optional[str]) -> Optional[Dict[str, Any]]:
        """Extract revenue information"""
        try:
            query = "What was the total revenue? Provide the exact number and year if mentioned."
            result = self.query_engine.query(query, document_filter=document_id)
            
            if result and result.get('answer'):
                answer = result['answer']
                
                # Extract numbers from answer
                numbers = self._extract_numbers(answer)
                years = self._extract_years(answer)
                
                if numbers:
                    return {
                        'value': numbers[0],
                        'year': years[0] if years else None,
                        'raw_answer': answer,
                        'sources': result.get('sources', [])
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting revenue: {e}")
            return None
    
    def _extract_profit(self, document_id: Optional[str]) -> Optional[Dict[str, Any]]:
        """Extract profit information"""
        try:
            query = "What was the profit or profit margin? Provide exact numbers."
            result = self.query_engine.query(query, document_filter=document_id)
            
            if result and result.get('answer'):
                answer = result['answer']
                numbers = self._extract_numbers(answer)
                years = self._extract_years(answer)
                
                if numbers:
                    return {
                        'value': numbers[0],
                        'year': years[0] if years else None,
                        'raw_answer': answer,
                        'sources': result.get('sources', [])
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting profit: {e}")
            return None
    
    def _extract_margin(self, document_id: Optional[str]) -> Optional[Dict[str, Any]]:
        """Extract margin information"""
        try:
            query = "What was the profit margin percentage?"
            result = self.query_engine.query(query, document_filter=document_id)
            
            if result and result.get('answer'):
                answer = result['answer']
                
                # Look for percentages
                percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', answer)
                years = self._extract_years(answer)
                
                if percentages:
                    return {
                        'value': float(percentages[0]),
                        'year': years[0] if years else None,
                        'unit': '%',
                        'raw_answer': answer,
                        'sources': result.get('sources', [])
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting margin: {e}")
            return None
    
    def _extract_product_metrics(self, document_id: Optional[str]) -> Optional[List[Dict[str, Any]]]:
        """Extract product performance metrics"""
        try:
            query = "List all products mentioned with their sales figures and performance metrics."
            result = self.query_engine.query(query, document_filter=document_id, top_k=10)
            
            if result and result.get('answer'):
                answer = result['answer']
                
                # Try to parse product data
                products = []
                
                # Look for common patterns like "Product A: 35 lakhs"
                product_pattern = r'Product\s+([A-Z]|[A-Z]\w+)[\s:]+.*?(\d+(?:\.\d+)?)\s*(?:lakhs?|crores?|million)?'
                matches = re.finditer(product_pattern, answer, re.IGNORECASE)
                
                for match in matches:
                    products.append({
                        'name': f"Product {match.group(1)}",
                        'sales': float(match.group(2)),
                        'unit': 'lakhs'
                    })
                
                if products:
                    return products
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting product metrics: {e}")
            return None
    
    def _extract_regional_metrics(self, document_id: Optional[str]) -> Optional[List[Dict[str, Any]]]:
        """Extract regional performance metrics"""
        try:
            query = "List all regions mentioned with their sales figures and growth rates."
            result = self.query_engine.query(query, document_filter=document_id, top_k=10)
            
            if result and result.get('answer'):
                answer = result['answer']
                
                regions = []
                
                # Look for region patterns
                region_pattern = r'Region\s+([A-Z])[\s:]+.*?(\d+(?:\.\d+)?)\s*(?:lakhs?|crores?)?'
                matches = re.finditer(region_pattern, answer, re.IGNORECASE)
                
                for match in matches:
                    regions.append({
                        'name': f"Region {match.group(1)}",
                        'sales': float(match.group(2)),
                        'unit': 'lakhs'
                    })
                
                if regions:
                    return regions
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting regional metrics: {e}")
            return None
    
    def _calculate_growth_rates(self, kpis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Calculate growth rates from KPIs"""
        try:
            growth = {}
            
            # Example: If we have revenue for multiple years
            if 'revenue' in kpis and 'value' in kpis['revenue']:
                # Placeholder for growth calculation
                # In real scenario, would need historical data
                growth['revenue_growth'] = {
                    'value': None,
                    'note': 'Requires historical data for calculation'
                }
            
            return growth if growth else None
            
        except Exception as e:
            logger.error(f"Error calculating growth rates: {e}")
            return None
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numerical values from text"""
        # Pattern for numbers including decimals and with units like lakhs/crores
        pattern = r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakhs?|crores?|million|billion)?'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        numbers = []
        for match in matches:
            try:
                # Remove commas and convert to float
                num = float(match.replace(',', ''))
                numbers.append(num)
            except:
                continue
        
        return numbers
    
    def _extract_years(self, text: str) -> List[int]:
        """Extract years from text"""
        pattern = r'\b(20\d{2})\b'
        matches = re.findall(pattern, text)
        return [int(year) for year in matches]
    
    def get_summary_stats(self, document_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get summary statistics from documents
        
        Args:
            document_id: Optional document ID
            
        Returns:
            Summary statistics dictionary
        """
        try:
            kpis = self.extract_kpis(document_id)
            
            summary = {
                'total_kpis': len(kpis),
                'has_revenue': 'revenue' in kpis,
                'has_profit': 'profit' in kpis,
                'has_margin': 'margin' in kpis,
                'has_products': 'products' in kpis,
                'has_regions': 'regions' in kpis,
                'extracted_at': datetime.utcnow().isoformat()
            }
            
            if 'products' in kpis and kpis['products']:
                summary['product_count'] = len(kpis['products'])
            
            if 'regions' in kpis and kpis['regions']:
                summary['region_count'] = len(kpis['regions'])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting summary stats: {e}")
            return {}
    
    def analyze_trends(self, kpis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze trends from KPI data
        
        Args:
            kpis: KPI dictionary
            
        Returns:
            Trend analysis
        """
        try:
            trends = {}
            
            # Product trends
            if 'products' in kpis and kpis['products']:
                products = kpis['products']
                sorted_products = sorted(products, key=lambda x: x.get('sales', 0), reverse=True)
                
                trends['top_product'] = sorted_products[0] if sorted_products else None
                trends['bottom_product'] = sorted_products[-1] if sorted_products else None
            
            # Regional trends
            if 'regions' in kpis and kpis['regions']:
                regions = kpis['regions']
                sorted_regions = sorted(regions, key=lambda x: x.get('sales', 0), reverse=True)
                
                trends['top_region'] = sorted_regions[0] if sorted_regions else None
                trends['bottom_region'] = sorted_regions[-1] if sorted_regions else None
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {}


# Global analytics engine instance
analytics_engine = None


def get_analytics_engine() -> AnalyticsEngine:
    """Get or create global analytics engine instance"""
    global analytics_engine
    if analytics_engine is None:
        analytics_engine = AnalyticsEngine()
    return analytics_engine
