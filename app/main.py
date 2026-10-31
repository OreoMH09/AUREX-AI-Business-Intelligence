"""
AUREX FastAPI Application
Main entry point for the backend API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core import settings, logger
from app.api.routes import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Create necessary directories
    import os
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multimodal RAG-Based Business Intelligence and Decision Support System",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# Include routers
from app.api.routes import documents, query, analytics, visualization, reports, evaluation

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(visualization.router, prefix="/api/visualization", tags=["Visualization"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(evaluation.router, prefix="/api", tags=["Evaluation"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Multimodal RAG-Based Business Intelligence and Decision Support System",
        "docs": "/api/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
