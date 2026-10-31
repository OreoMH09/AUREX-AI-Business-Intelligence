"""
Evaluation API routes
Endpoints for system evaluation and metrics
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from app.evaluation import get_evaluation_metrics

logger = logging.getLogger("aurex.api.evaluation")

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.get("/metrics")
async def get_metrics():
    """
    Get aggregate evaluation metrics
    
    Returns:
        Aggregate statistics across all evaluations
    """
    try:
        metrics = get_evaluation_metrics()
        aggregate = metrics.get_aggregate_metrics()
        
        return {
            "success": True,
            "metrics": aggregate
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def get_recent_results(limit: int = 10):
    """
    Get recent evaluation results
    
    Args:
        limit: Number of recent results to return (default: 10)
    
    Returns:
        List of recent evaluation results
    """
    try:
        metrics = get_evaluation_metrics()
        results = metrics.get_latest_results(n=limit)
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error getting results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear")
async def clear_results():
    """
    Clear all evaluation results
    
    Returns:
        Success confirmation
    """
    try:
        metrics = get_evaluation_metrics()
        metrics.clear_results()
        
        return {
            "success": True,
            "message": "Evaluation results cleared"
        }
        
    except Exception as e:
        logger.error(f"Error clearing results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def evaluation_health():
    """
    Check evaluation system health
    
    Returns:
        Health status
    """
    try:
        metrics = get_evaluation_metrics()
        aggregate = metrics.get_aggregate_metrics()
        
        return {
            "status": "healthy",
            "total_evaluations": aggregate.get("total_queries", 0),
            "evaluation_active": True
        }
        
    except Exception as e:
        logger.error(f"Evaluation health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "evaluation_active": False
        }
