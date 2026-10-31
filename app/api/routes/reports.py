"""
AUREX Reports API Routes
Endpoints for report generation and download
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path

from app.reports.generator import get_report_generator
from app.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


class ReportRequest(BaseModel):
    """Report generation request"""
    document_id: Optional[str] = None
    report_type: str = 'executive'
    format: str = 'html'


class ReportResponse(BaseModel):
    """Report generation response"""
    success: bool
    filename: Optional[str] = None
    report_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a business report
    
    Args:
        request: Report generation request
        
    Returns:
        Report metadata and content
    """
    try:
        logger.info(f"Report generation requested: {request.report_type}, format: {request.format}")
        
        report_gen = get_report_generator()
        result = report_gen.generate_report(
            document_id=request.document_id,
            report_type=request.report_type,
            format=request.format
        )
        
        return ReportResponse(**result)
        
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_report(filename: str):
    """
    Download a generated report
    
    Args:
        filename: Report filename
        
    Returns:
        File download response
    """
    try:
        logger.info(f"Report download requested: {filename}")
        
        report_path = Path("data/reports") / filename
        
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        return FileResponse(
            path=report_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Error downloading report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview/{filename}", response_class=HTMLResponse)
async def preview_report(filename: str):
    """
    Preview a generated HTML report
    
    Args:
        filename: Report filename
        
    Returns:
        HTML content for preview
    """
    try:
        logger.info(f"Report preview requested: {filename}")
        
        report_path = Path("data/reports") / filename
        
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        if not filename.endswith('.html'):
            raise HTTPException(status_code=400, detail="Only HTML reports can be previewed")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HTMLResponse(content=content)
        
    except Exception as e:
        logger.error(f"Error previewing report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{filename}")
async def delete_report(filename: str):
    """
    Delete a generated report
    
    Args:
        filename: Report filename
        
    Returns:
        Success confirmation
    """
    try:
        logger.info(f"Report deletion requested: {filename}")
        
        report_path = Path("data/reports") / filename
        
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Delete the file
        report_path.unlink()
        
        logger.info(f"Report deleted successfully: {filename}")
        return {"success": True, "message": f"Report {filename} deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
