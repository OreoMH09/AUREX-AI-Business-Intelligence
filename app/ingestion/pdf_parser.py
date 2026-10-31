"""
AUREX PDF Parser
Extract text, tables, and metadata from PDF documents
"""
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid

import fitz  # PyMuPDF
from PIL import Image
import io

from app.ingestion.base import BaseParser, ParsedDocument, DocumentChunk
from app.models import DocumentMetadata, FileType
from app.core import get_logger

logger = get_logger(__name__)


class PDFParser(BaseParser):
    """Parser for PDF documents"""
    
    def __init__(self, enable_ocr: bool = False):
        """
        Initialize PDF parser
        
        Args:
            enable_ocr: Enable OCR for scanned documents (requires tesseract)
        """
        super().__init__()
        self.supported_extensions = ['.pdf']
        self.enable_ocr = enable_ocr
        
        if enable_ocr:
            try:
                import pytesseract
                self.ocr_available = True
                logger.info("OCR enabled for PDF parsing")
            except ImportError:
                self.ocr_available = False
                logger.warning("pytesseract not available, OCR disabled")
        else:
            self.ocr_available = False
    
    def parse(self, file_path: Path) -> ParsedDocument:
        """
        Parse PDF document
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            ParsedDocument with extracted content
        """
        logger.info(f"Parsing PDF: {file_path}")
        
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid PDF file: {file_path}")
        
        try:
            # Open PDF
            doc = fitz.open(file_path)
            
            # Extract text from all pages
            text_parts = []
            sections = []
            tables = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                page_text = page.get_text()
                
                # If page is empty and OCR is enabled, try OCR
                if not page_text.strip() and self.ocr_available:
                    page_text = self._ocr_page(page)
                
                if page_text.strip():
                    text_parts.append(page_text)
                    
                    # Try to extract sections (headings)
                    page_sections = self._extract_sections(page_text, page_num + 1)
                    sections.extend(page_sections)
                
                # Try to extract tables
                page_tables = self._extract_tables(page, page_num + 1)
                tables.extend(page_tables)
            
            # Combine all text
            full_text = "\n\n".join(text_parts)
            
            # Create chunks from pages
            chunks = []
            for page_num, page_text in enumerate(text_parts):
                if page_text.strip():
                    chunk = DocumentChunk(
                        chunk_id=f"page_{page_num + 1}",
                        content=page_text,
                        metadata={"page_number": page_num + 1, "chunk_type": "page"},
                        page_number=page_num + 1
                    )
                    chunks.append(chunk)
            
            # Extract metadata
            metadata_dict = {
                "filename": file_path.name,
                "file_type": "pdf",
                "page_count": len(doc),
                "file_size": self.get_file_size(file_path),
                "parsed_at": datetime.utcnow().isoformat()
            }
            
            # Close document
            doc.close()
            
            # Create parsed document
            parsed_doc = ParsedDocument(
                text=full_text,
                chunks=chunks,
                metadata=metadata_dict,
                tables=tables,
                sections=sections,
                page_count=len(text_parts)
            )
            
            logger.info(f"PDF parsed successfully: {len(text_parts)} pages, "
                       f"{len(tables)} tables, {len(sections)} sections")
            
            return parsed_doc
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}", exc_info=True)
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    def extract_metadata(self, file_path: Path) -> DocumentMetadata:
        """
        Extract metadata from PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            DocumentMetadata object
        """
        try:
            doc = fitz.open(file_path)
            pdf_metadata = doc.metadata
            
            # Extract year from metadata or filename
            year = self._extract_year(pdf_metadata, file_path)
            
            metadata = DocumentMetadata(
                document_id=str(uuid.uuid4()),
                filename=file_path.name,
                file_type=FileType.PDF,
                year=year,
                created_at=datetime.utcnow()
            )
            
            doc.close()
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {e}")
            # Return basic metadata
            return DocumentMetadata(
                document_id=str(uuid.uuid4()),
                filename=file_path.name,
                file_type=FileType.PDF,
                created_at=datetime.utcnow()
            )
    
    def _extract_sections(self, text: str, page_num: int) -> List[Dict[str, str]]:
        """
        Extract sections/headings from text
        
        Args:
            text: Page text
            page_num: Page number
            
        Returns:
            List of sections
        """
        sections = []
        
        # Simple heuristic: lines that are short, capitalized, or numbered
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if line looks like a heading
            if self._is_likely_heading(line):
                sections.append({
                    "title": line,
                    "page": page_num
                })
        
        return sections
    
    def _is_likely_heading(self, line: str) -> bool:
        """
        Check if a line is likely a heading
        
        Args:
            line: Text line
            
        Returns:
            True if likely a heading
        """
        # Too long to be a heading
        if len(line) > 100:
            return False
        
        # Too short
        if len(line) < 3:
            return False
        
        # Contains common heading patterns
        heading_patterns = [
            r'^\d+\.\s+[A-Z]',  # 1. Chapter
            r'^Chapter\s+\d+',   # Chapter 1
            r'^Section\s+\d+',   # Section 1
            r'^[IVX]+\.\s+',     # Roman numerals
            r'^[A-Z][A-Z\s]+$',  # ALL CAPS (but not too long)
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, line):
                return True
        
        # Mostly uppercase and short
        if line.isupper() and len(line) < 50:
            return True
        
        return False
    
    def _extract_tables(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """
        Extract tables from PDF page
        
        Args:
            page: PyMuPDF page object
            page_num: Page number
            
        Returns:
            List of tables
        """
        tables = []
        
        try:
            # PyMuPDF table extraction (basic)
            # This is a simple implementation - can be enhanced with more sophisticated methods
            
            # Get text in blocks
            blocks = page.get_text("blocks")
            
            # Look for table-like structures
            # This is a simplified approach - real table extraction is complex
            table_candidates = []
            
            for block in blocks:
                if len(block) >= 5:  # Block has text
                    text = block[4]
                    
                    # Check if text has table-like structure (multiple columns)
                    if '\t' in text or '|' in text:
                        table_candidates.append({
                            "page": page_num,
                            "text": text,
                            "bbox": block[:4]
                        })
            
            # Convert candidates to structured tables
            for idx, candidate in enumerate(table_candidates):
                tables.append({
                    "table_id": f"table_{page_num}_{idx}",
                    "page": page_num,
                    "content": candidate["text"],
                    "type": "extracted"
                })
        
        except Exception as e:
            logger.warning(f"Error extracting tables from page {page_num}: {e}")
        
        return tables
    
    def _ocr_page(self, page: fitz.Page) -> str:
        """
        Perform OCR on a PDF page
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            OCR text
        """
        if not self.ocr_available:
            return ""
        
        try:
            import pytesseract
            
            # Convert page to image
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Perform OCR
            text = pytesseract.image_to_string(img)
            return text
            
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return ""
    
    def _extract_year(self, pdf_metadata: Dict, file_path: Path) -> Optional[int]:
        """
        Extract year from PDF metadata or filename
        
        Args:
            pdf_metadata: PDF metadata dictionary
            file_path: Path to file
            
        Returns:
            Extracted year or None
        """
        # Try metadata creation date
        if pdf_metadata and 'creationDate' in pdf_metadata:
            try:
                # Parse date string (format: D:20240101...)
                date_str = pdf_metadata['creationDate']
                if date_str.startswith('D:'):
                    year_str = date_str[2:6]
                    return int(year_str)
            except:
                pass
        
        # Try filename
        filename = file_path.stem
        year_pattern = r'20\d{2}'  # Match years 2000-2099
        matches = re.findall(year_pattern, filename)
        
        if matches:
            return int(matches[-1])  # Return last match
        
        return None
    
    def extract_text_by_page(self, file_path: Path) -> List[Tuple[int, str]]:
        """
        Extract text page by page
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of (page_number, text) tuples
        """
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid PDF file: {file_path}")
        
        pages = []
        doc = fitz.open(file_path)
        
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                if not text.strip() and self.ocr_available:
                    text = self._ocr_page(page)
                
                pages.append((page_num + 1, text))
            
            return pages
            
        finally:
            doc.close()
