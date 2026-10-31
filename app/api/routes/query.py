"""
AUREX Query API Routes
Endpoints for RAG-based question answering
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.rag.query_engine import get_query_engine
from app.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


class QueryRequest(BaseModel):
    """Query request model"""
    question: str = Field(..., description="User question")
    top_k: Optional[int] = Field(None, description="Number of documents to retrieve")
    document_filter: Optional[str] = Field(None, description="Filter by document ID")


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    sources: List[Dict[str, Any]]
    retrieved_chunks: int
    processing_time_ms: int
    timestamp: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """RAG health check response"""
    vector_store: str
    llm: str
    overall: str
    vector_store_chunks: Optional[int] = None


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query documents using RAG
    
    Args:
        request: Query request with question and optional parameters
        
    Returns:
        Answer with sources and metadata
    """
    try:
        logger.info(f"Received query: {request.question}")
        
        # Get query engine
        query_engine = get_query_engine()
        
        # Process query with REAL RAG
        result = query_engine.query(
            question=request.question,
            top_k=request.top_k or 3,  # Default to 3 for speed
            document_filter=request.document_filter
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rag-health", response_model=HealthCheckResponse)
async def check_rag_health():
    """
    Check RAG system health
    
    Returns:
        Health status of vector store and LLM
    """
    try:
        query_engine = get_query_engine()
        health = query_engine.check_health()
        
        return HealthCheckResponse(**health)
        
    except Exception as e:
        logger.error(f"Error checking RAG health: {e}")
        raise HTTPException(status_code=500, detail=str(e))
