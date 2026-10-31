"""
AUREX Health Check Endpoint
System health and status checks
"""
from fastapi import APIRouter
from app.core import settings, logger
from app.models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns system status and service availability
    """
    logger.info("Health check requested")
    
    services_status = {}
    
    # Check vector database
    try:
        from app.vector_store.chroma_store import get_vector_store
        vector_store = get_vector_store()
        # Try to get collection info
        collection_count = vector_store.collection.count()
        services_status["vector_db"] = "healthy"
        logger.debug(f"Vector DB healthy: {collection_count} documents")
    except Exception as e:
        logger.warning(f"Vector DB health check failed: {e}")
        services_status["vector_db"] = "unavailable"
    
    # Check LLM
    try:
        from app.llm.ollama_client import get_ollama_client
        ollama_client = get_ollama_client()
        # Check if Ollama server is reachable
        if ollama_client.check_health():
            services_status["llm"] = "healthy"
            logger.debug("LLM healthy")
        else:
            services_status["llm"] = "unavailable"
    except Exception as e:
        logger.warning(f"LLM health check failed: {e}")
        services_status["llm"] = "unavailable"
    
    # Check embeddings
    try:
        from app.vector_store.embeddings import get_embedding_service
        embeddings_service = get_embedding_service()
        # Check if model is loaded
        if embeddings_service.model:
            services_status["embeddings"] = "healthy"
            logger.debug("Embeddings healthy")
        else:
            services_status["embeddings"] = "unavailable"
    except Exception as e:
        logger.warning(f"Embeddings health check failed: {e}")
        services_status["embeddings"] = "unavailable"
    
    # Overall status based on critical services
    overall_status = "healthy"
    if services_status.get("vector_db") == "unavailable":
        overall_status = "degraded"
    
    return HealthResponse(
        status=overall_status,
        version=settings.app_version,
        environment=settings.environment,
        services=services_status
    )
