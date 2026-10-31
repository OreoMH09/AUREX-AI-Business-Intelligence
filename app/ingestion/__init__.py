"""
AUREX Ingestion Module
Document ingestion and parsing
"""
from app.ingestion.base import BaseParser
from app.ingestion.pdf_parser import PDFParser

__all__ = ["BaseParser", "PDFParser"]
