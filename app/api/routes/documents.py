"""
AUREX Document Routes
API endpoints for document management
"""
from typing import List
from pathlib import Path
import tempfile
import os

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models import (
    DocumentUploadResponse,
    DocumentInfo,
)
from app.ingestion.document_service import document_service
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload a document (PDF, Excel, CSV)
    
    The document will be saved and marked for ingestion.
    Ingestion happens in the background.
    """
    try:
        logger.info(f"Receiving file upload: {file.filename}")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # Read and write file content
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = Path(tmp_file.name)
        
        try:
            # Upload document
            response = await document_service.upload_document(
                file_path=tmp_file_path,
                original_filename=file.filename
            )
            
            # Schedule ingestion in background
            if background_tasks:
                background_tasks.add_task(
                    ingest_document_background,
                    response.document_id
                )
            
            return response
            
        finally:
            # Clean up temporary file
            if tmp_file_path.exists():
                tmp_file_path.unlink()
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/ingest/{document_id}")
async def ingest_document(document_id: str):
    """
    Manually trigger document ingestion
    
    Parses the document and extracts content.
    """
    try:
        logger.info(f"Manual ingestion triggered for: {document_id}")
        
        doc_info = await document_service.ingest_document(document_id)
        
        return {
            "message": "Document ingested successfully",
            "document": doc_info
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Ingestion error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """
    List all uploaded documents
    """
    try:
        documents = document_service.list_documents()
        return documents
    
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.get("/documents/{document_id}", response_model=DocumentInfo)
async def get_document(document_id: str):
    """
    Get document information by ID
    """
    try:
        doc_info = document_service.get_document(document_id)
        
        if not doc_info:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return doc_info
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to get document")


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document
    """
    try:
        success = document_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"message": "Document deleted successfully", "document_id": document_id}
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete document")


async def ingest_document_background(document_id: str):
    """Background task for document ingestion"""
    try:
        await document_service.ingest_document(document_id)
    except Exception as e:
        logger.error(f"Background ingestion failed for {document_id}: {e}")
