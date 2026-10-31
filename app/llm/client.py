"""
AUREX Unified LLM Client
Routes to appropriate LLM provider (Ollama, Gemini, or Groq)
"""
from typing import Optional
from app.core import settings, get_logger
from app.llm.ollama_client import get_ollama_client
from app.llm.gemini_client import get_gemini_client
from app.llm.groq_client import get_groq_client

logger = get_logger(__name__)


def get_llm_client():
    """
    Get the appropriate LLM client based on configuration
    
    Returns:
        LLM client instance (Ollama, Gemini, or Groq)
    """
    provider = settings.llm_provider.lower()
    
    if provider == "groq":
        logger.info("Using Groq LLM provider (ULTRA FAST!)")
        try:
            return get_groq_client()
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            logger.warning("Falling back to Ollama")
            return get_ollama_client()
    elif provider == "gemini":
        logger.info("Using Gemini LLM provider")
        try:
            return get_gemini_client()
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            logger.warning("Falling back to Ollama")
            return get_ollama_client()
    else:
        logger.info("Using Ollama LLM provider")
        return get_ollama_client()
