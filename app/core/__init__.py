"""
AUREX Core Module
Core application configuration and utilities
"""
from app.core.config import settings
from app.core.logging_config import logger, get_logger

__all__ = ["settings", "logger", "get_logger"]
