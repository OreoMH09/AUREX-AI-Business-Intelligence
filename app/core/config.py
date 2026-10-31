"""
AUREX Configuration Management
Centralized configuration using Pydantic Settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = Field(default="AUREX", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")
    
    # API
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=True, description="API auto-reload")
    
    # Streamlit
    streamlit_port: int = Field(default=8501, description="Streamlit port")
    
    # LLM Configuration
    llm_provider: str = Field(default="ollama", description="LLM provider")
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    ollama_model: str = Field(default="llama3.1:8b", description="Ollama model")
    llm_temperature: float = Field(default=0.1, description="LLM temperature")
    llm_max_tokens: int = Field(default=500, description="LLM max tokens")  # Reduced from 2000
    
    # Gemini Configuration
    gemini_api_key: str = Field(default="", description="Google Gemini API key")
    gemini_model: str = Field(default="gemini-1.5-flash", description="Gemini model")
    
    # Groq Configuration
    groq_api_key: str = Field(default="", description="Groq API key")
    groq_model: str = Field(default="llama-3.3-70b-versatile", description="Groq model")
    
    # Embeddings
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model"
    )
    embedding_dimension: int = Field(default=384, description="Embedding dimension")
    
    # Vector Database
    vector_db: str = Field(default="chromadb", description="Vector database")
    chroma_persist_dir: str = Field(default="./data/chroma_db", description="ChromaDB directory")
    collection_name: str = Field(default="aurex_documents", description="Collection name")
    
    # Retrieval
    top_k: int = Field(default=3, description="Top K retrieval")  # Reduced from 5 for speed
    similarity_threshold: float = Field(default=0.8, description="Similarity threshold")  # Increased for better matches
    enable_reranking: bool = Field(default=False, description="Enable reranking")
    
    # Chunking
    chunk_size: int = Field(default=512, description="Chunk size")
    chunk_overlap: int = Field(default=50, description="Chunk overlap")
    
    # File Upload
    max_file_size_mb: int = Field(default=50, description="Max file size in MB")
    allowed_extensions: str = Field(default="pdf,xlsx,xls,csv", description="Allowed extensions")
    upload_dir: str = Field(default="./data/raw", description="Upload directory")
    
    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/aurex.db",
        description="Database URL"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_file: str = Field(default="./logs/aurex.log", description="Log file")
    
    # Analytics
    enable_analytics: bool = Field(default=True, description="Enable analytics")
    enable_visualization: bool = Field(default=True, description="Enable visualization")
    
    # Agent
    max_tool_calls: int = Field(default=10, description="Max tool calls")
    agent_timeout_seconds: int = Field(default=15, description="Agent timeout")  # Reduced to 15 seconds
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key"
    )
    allowed_origins: str = Field(
        default="http://localhost:8501,http://localhost:8000",
        description="Allowed CORS origins"
    )
    
    # OCR
    tesseract_path: Optional[str] = Field(default=None, description="Tesseract path")
    enable_ocr: bool = Field(default=False, description="Enable OCR")
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed extensions as list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed origins as list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes"""
        return self.max_file_size_mb * 1024 * 1024
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
