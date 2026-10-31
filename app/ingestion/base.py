"""
AUREX Base Parser
Abstract base class for document parsers
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from app.models import DocumentMetadata, FileType


@dataclass
class DocumentChunk:
    """Represents a chunk of document content"""
    chunk_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    page_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "metadata": self.metadata or {},
            "page_number": self.page_number
        }


class ParsedDocument:
    """Container for parsed document data"""
    
    def __init__(
        self,
        text: str,
        chunks: Optional[List[DocumentChunk]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tables: Optional[List[Dict[str, Any]]] = None,
        sections: Optional[List[Dict[str, str]]] = None,
        page_count: Optional[int] = None,
        raw_data: Optional[Any] = None
    ):
        self.text = text
        self.chunks = chunks or []
        self.metadata = metadata or {}
        self.tables = tables or []
        self.sections = sections or []
        self.page_count = page_count
        self.raw_data = raw_data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "text": self.text,
            "chunks": [chunk.to_dict() for chunk in self.chunks],
            "metadata": self.metadata,
            "tables": self.tables,
            "sections": self.sections,
            "page_count": self.page_count,
            "has_tables": len(self.tables) > 0,
            "text_length": len(self.text),
            "num_sections": len(self.sections),
            "num_chunks": len(self.chunks)
        }


class BaseParser(ABC):
    """Abstract base class for document parsers"""
    
    def __init__(self):
        self.supported_extensions: List[str] = []
    
    @abstractmethod
    def parse(self, file_path: Path) -> ParsedDocument:
        """
        Parse a document and extract content
        
        Args:
            file_path: Path to the document file
            
        Returns:
            ParsedDocument with extracted content
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
            Exception: For parsing errors
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> DocumentMetadata:
        """
        Extract metadata from document
        
        Args:
            file_path: Path to the document file
            
        Returns:
            DocumentMetadata object
        """
        pass
    
    def validate_file(self, file_path: Path) -> bool:
        """
        Validate if file exists and has supported extension
        
        Args:
            file_path: Path to the document file
            
        Returns:
            True if valid, False otherwise
        """
        if not file_path.exists():
            return False
        
        if not file_path.is_file():
            return False
        
        if self.supported_extensions:
            return file_path.suffix.lower() in self.supported_extensions
        
        return True
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        return file_path.stat().st_size
