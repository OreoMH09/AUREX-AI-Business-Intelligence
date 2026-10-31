"""
AUREX Visualization API Routes
Endpoints for chart generation
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.analytics.engine import get_analytics_engine
from app.visualization.engine import get_visualization_engine
from app.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


class ChartRequest(BaseModel):
    """Chart creation request"""
    data: Dict[str, Any]
    chart_type: str = 'auto'
    title: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class ChartResponse(BaseModel):
    """Chart response"""
    chart: str
    chart_type: str
    title: Optional[str] = None
    created_at: str


class KPIChartsResponse(BaseModel):
    """KPI charts response"""
    charts: List[Dict[str, Any]]
    chart_count: int


@router.post("/chart", response_model=ChartResponse)
async def create_chart(request: ChartRequest):
    """
    Create a custom chart from data
    
    Args:
        request: Chart request with data and options
        
    Returns:
        Chart as JSON
    """
    try:
        logger.info(f"Chart creation requested: {request.chart_type}")
        
        viz_engine = get_visualization_engine()
        
        options = request.options or {}
        chart_data = viz_engine.create_chart(
            data=request.data,
            chart_type=request.chart_type,
            title=request.title,
            **options
        )
        
        if not chart_data:
            raise HTTPException(status_code=500, detail="Failed to create chart")
        
        return ChartResponse(
            chart=chart_data['chart'],
            chart_type=chart_data['chart_type'],
            title=request.title,
            created_at=chart_data['created_at']
        )
        
    except Exception as e:
        logger.error(f"Error creating chart: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kpi-charts", response_model=KPIChartsResponse)
async def get_kpi_charts(
    document_id: Optional[str] = Query(None, description="Filter by document ID")
):
    """
    Get charts for all KPIs
    
    Args:
        document_id: Optional document ID to filter
        
    Returns:
        List of charts for KPIs
    """
    try:
        logger.info(f"KPI charts requested for document: {document_id}")
        
        # Get KPIs
        analytics_engine = get_analytics_engine()
        kpis = analytics_engine.extract_kpis(document_id)
        
        if not kpis:
            return KPIChartsResponse(charts=[], chart_count=0)
        
        # Create charts
        viz_engine = get_visualization_engine()
        charts = viz_engine.create_kpi_charts(kpis)
        
        return KPIChartsResponse(
            charts=charts,
            chart_count=len(charts)
        )
        
    except Exception as e:
        logger.error(f"Error creating KPI charts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
