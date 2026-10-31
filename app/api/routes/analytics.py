"""
AUREX Analytics API Routes
Endpoints for automated KPI extraction and analysis
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.analytics.engine import get_analytics_engine
from app.analytics.advanced import get_advanced_analytics
from app.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


class KPIResponse(BaseModel):
    """KPI extraction response"""
    kpis: Dict[str, Any]
    document_id: Optional[str] = None


class SummaryStatsResponse(BaseModel):
    """Summary statistics response"""
    stats: Dict[str, Any]


class TrendAnalysisResponse(BaseModel):
    """Trend analysis response"""
    trends: Dict[str, Any]
    kpis: Dict[str, Any]


@router.get("/kpis", response_model=KPIResponse)
async def extract_kpis(
    document_id: Optional[str] = Query(None, description="Filter by document ID")
):
    """
    Extract KPIs from documents
    
    Args:
        document_id: Optional document ID to filter
        
    Returns:
        Extracted KPIs with metadata
    """
    try:
        logger.info(f"KPI extraction requested for document: {document_id}")
        
        analytics_engine = get_analytics_engine()
        kpis = analytics_engine.extract_kpis(document_id)
        
        return KPIResponse(kpis=kpis, document_id=document_id)
        
    except Exception as e:
        logger.error(f"Error extracting KPIs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary", response_model=SummaryStatsResponse)
async def get_summary_stats(
    document_id: Optional[str] = Query(None, description="Filter by document ID")
):
    """
    Get summary statistics
    
    Args:
        document_id: Optional document ID to filter
        
    Returns:
        Summary statistics
    """
    try:
        logger.info(f"Summary stats requested for document: {document_id}")
        
        analytics_engine = get_analytics_engine()
        stats = analytics_engine.get_summary_stats(document_id)
        
        return SummaryStatsResponse(stats=stats)
        
    except Exception as e:
        logger.error(f"Error getting summary stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends", response_model=TrendAnalysisResponse)
async def analyze_trends(
    document_id: Optional[str] = Query(None, description="Filter by document ID")
):
    """
    Analyze trends from KPIs
    
    Args:
        document_id: Optional document ID to filter
        
    Returns:
        Trend analysis with KPIs
    """
    try:
        logger.info(f"Trend analysis requested for document: {document_id}")
        
        analytics_engine = get_analytics_engine()
        kpis = analytics_engine.extract_kpis(document_id)
        trends = analytics_engine.analyze_trends(kpis)
        
        return TrendAnalysisResponse(trends=trends, kpis=kpis)
        
    except Exception as e:
        logger.error(f"Error analyzing trends: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



class ComparisonRequest(BaseModel):
    """Period comparison request"""
    period1: str
    period2: str
    metric: str = 'revenue'
    document_id: Optional[str] = None


class ScenarioRequest(BaseModel):
    """Scenario analysis request"""
    baseline: Dict[str, float]
    scenarios: List[Dict[str, Any]]


class ProjectionRequest(BaseModel):
    """Trend projection request"""
    historical_data: List[Dict[str, Any]]
    periods_ahead: int = 3


@router.post("/compare")
async def compare_periods(request: ComparisonRequest):
    """
    Compare metrics between two periods
    
    Args:
        request: Comparison request with periods and metric
        
    Returns:
        Comparison results with change calculations
    """
    try:
        logger.info(f"Period comparison requested: {request.period1} vs {request.period2}")
        
        advanced = get_advanced_analytics()
        result = advanced.compare_periods(
            period1=request.period1,
            period2=request.period2,
            metric=request.metric,
            document_id=request.document_id
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error comparing periods: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yoy")
async def year_over_year(
    base_year: int = Query(..., description="Base year for comparison"),
    metric: str = Query('revenue', description="Metric to analyze"),
    document_id: Optional[str] = Query(None, description="Filter by document ID")
):
    """
    Year-over-year analysis
    
    Args:
        base_year: Base year for comparison
        metric: Metric to analyze
        document_id: Optional document filter
        
    Returns:
        Year-over-year comparison
    """
    try:
        logger.info(f"YoY analysis requested for {metric}, base year: {base_year}")
        
        advanced = get_advanced_analytics()
        result = advanced.year_over_year(
            base_year=base_year,
            metric=metric,
            document_id=document_id
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in YoY analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scenario")
async def scenario_analysis(request: ScenarioRequest):
    """
    What-if scenario analysis
    
    Args:
        request: Scenario request with baseline and scenarios
        
    Returns:
        Scenario analysis with projections
    """
    try:
        logger.info(f"Scenario analysis requested with {len(request.scenarios)} scenarios")
        
        advanced = get_advanced_analytics()
        result = advanced.scenario_analysis(
            baseline=request.baseline,
            scenarios=request.scenarios
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in scenario analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projection")
async def trend_projection(request: ProjectionRequest):
    """
    Project future trends
    
    Args:
        request: Projection request with historical data
        
    Returns:
        Trend projections
    """
    try:
        logger.info(f"Trend projection requested for {request.periods_ahead} periods")
        
        advanced = get_advanced_analytics()
        result = advanced.trend_projection(
            historical_data=request.historical_data,
            periods_ahead=request.periods_ahead
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in trend projection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
