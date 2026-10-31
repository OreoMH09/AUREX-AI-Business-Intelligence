"""
AUREX Logging Configuration
Structured logging setup for the application
"""
import logging
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """
    Setup application logging with both console and file handlers
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("aurex")
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with simple format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler with JSON format
    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setLevel(getattr(logging, settings.log_level.upper()))
    json_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(json_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Global logger instance
logger = setup_logging()


def get_logger(name: str) -> logging.Logger:
    """
    Get a child logger with the specified name
    
    Args:
        name: Logger name
        
    Returns:
        Child logger instance
    """
    return logger.getChild(name)
