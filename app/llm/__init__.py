"""
AUREX LLM Package
"""
from app.llm.ollama_client import OllamaClient, get_ollama_client
from app.llm.prompts import (
    BUSINESS_ANALYST_SYSTEM_PROMPT,
    build_rag_prompt,
    build_summary_prompt,
    build_analysis_prompt,
    build_comparison_prompt
)

__all__ = [
    "OllamaClient",
    "get_ollama_client",
    "BUSINESS_ANALYST_SYSTEM_PROMPT",
    "build_rag_prompt",
    "build_summary_prompt",
    "build_analysis_prompt",
    "build_comparison_prompt"
]
