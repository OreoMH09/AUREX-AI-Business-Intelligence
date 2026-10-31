"""
AUREX Document Service
Manages document uploads, ingestion, and storage
"""
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from app.ingestion.pdf_parser import PDFParser
from app.ingestion.excel_parser import ExcelParser
from app.ingestion.csv_parser import CSVParser
from app.ingestion.base import ParsedDocument
from app.vector_store.chroma_store import get_vector_store
from app.models import (
    FileType,
    DocumentStatus,
    DocumentInfo,
    DocumentUploadResponse,
    DocumentMetadata
)
from app.core import settings, get_logger

logger = get_logger(__name__)


class DocumentService:
    """Service for document management"""
    
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize parsers
        self.pdf_parser = PDFParser(enable_ocr=settings.enable_ocr)
        self.excel_parser = ExcelParser()
        self.csv_parser = CSVParser()
        
        # Initialize vector store
        try:
            self.vector_store = get_vector_store()
        except Exception as e:
            logger.warning(f"Vector store initialization failed: {e}. Will continue without it.")
            self.vector_store = None
        
        # Document registry (in-memory for now, will use DB later)
        self.documents: Dict[str, DocumentInfo] = {}
        
        # Discover existing documents on startup
        self._discover_existing_documents()
        
        # Auto-ingest discovered documents (async, non-blocking)
        self._schedule_auto_ingestion()
        
        logger.info(f"DocumentService initialized with {len(self.documents)} documents")
    
    async def upload_document(
        self,
        file_path: Path,
        original_filename: str
    ) -> DocumentUploadResponse:
        """
        Upload and save a document
        
        Args:
            file_path: Temporary file path
            original_filename: Original filename
            
        Returns:
            DocumentUploadResponse
        """
        try:
            logger.info(f"Uploading document: {original_filename}")
            
            # Validate file
            file_ext = Path(original_filename).suffix.lower()
            # Remove the leading dot for comparison
            file_ext_no_dot = file_ext.lstrip('.')
            if file_ext_no_dot not in settings.allowed_extensions_list:
                raise ValueError(f"File type not supported: {file_ext}")
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > settings.max_file_size_bytes:
                raise ValueError(
                    f"File too large: {file_size} bytes "
                    f"(max: {settings.max_file_size_bytes} bytes)"
                )
            
            # Determine file type
            file_type = self._determine_file_type(file_ext)
            
            # Generate document ID
            doc_id = str(uuid.uuid4())
            
            # Save file
            safe_filename = self._sanitize_filename(original_filename)
            dest_path = self.upload_dir / f"{doc_id}_{safe_filename}"
            shutil.copy2(file_path, dest_path)
            
            # Create document info
            doc_info = DocumentInfo(
                document_id=doc_id,
                filename=original_filename,
                file_type=file_type,
                file_size_bytes=file_size,
                status=DocumentStatus.PENDING,
                uploaded_at=datetime.utcnow()
            )
            
            # Store in registry
            self.documents[doc_id] = doc_info
            
            logger.info(f"Document uploaded successfully: {doc_id}")
            
            return DocumentUploadResponse(
                document_id=doc_id,
                filename=original_filename,
                file_type=file_type,
                file_size_bytes=file_size,
                status=DocumentStatus.PENDING,
                message="Document uploaded successfully"
            )
            
        except Exception as e:
            logger.error(f"Error uploading document: {e}", exc_info=True)
            raise  # Re-raise original exception
    
    async def ingest_document(self, document_id: str) -> DocumentInfo:
        """
        Ingest and parse a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Updated DocumentInfo
        """
        try:
            logger.info(f"Ingesting document: {document_id}")
            
            # Get document info
            if document_id not in self.documents:
                raise ValueError(f"Document not found: {document_id}")
            
            doc_info = self.documents[document_id]
            
            # Update status
            doc_info.status = DocumentStatus.PROCESSING
            
            # Get file path
            file_path = self._get_document_path(document_id, doc_info.filename)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Document file not found: {file_path}")
            
            # Parse based on file type
            parsed_doc = None
            
            if doc_info.file_type == FileType.PDF:
                parsed_doc = self.pdf_parser.parse(file_path)
            elif doc_info.file_type == FileType.EXCEL:
                parsed_doc = self.excel_parser.parse(file_path)
            elif doc_info.file_type == FileType.CSV:
                parsed_doc = self.csv_parser.parse(file_path)
            else:
                raise ValueError(f"Unsupported file type: {doc_info.file_type}")
            
            # Update document info with parsed data
            if parsed_doc:
                # Store chunks in vector database
                if self.vector_store and parsed_doc.chunks:
                    try:
                        logger.info(f"Storing {len(parsed_doc.chunks)} chunks in vector store")
                        chunks_added = self.vector_store.add_documents(
                            chunks=parsed_doc.chunks,
                            document_id=document_id
                        )
                        logger.info(f"Added {chunks_added} chunks to vector store")
                    except Exception as e:
                        logger.error(f"Error storing chunks in vector store: {e}")
                        # Continue even if vector store fails
                
                doc_info.status = DocumentStatus.COMPLETED
                doc_info.processed_at = datetime.utcnow()
                doc_info.metadata = parsed_doc.to_dict()
                
                logger.info(f"Document ingested successfully: {document_id}")
            else:
                doc_info.status = DocumentStatus.FAILED
                logger.error(f"Failed to parse document: {document_id}")
            
            return doc_info
            
        except Exception as e:
            logger.error(f"Error ingesting document {document_id}: {e}", exc_info=True)
            
            # Update status to failed
            if document_id in self.documents:
                self.documents[document_id].status = DocumentStatus.FAILED
            
            raise  # Re-raise original exception
    
    def get_document(self, document_id: str) -> Optional[DocumentInfo]:
        """Get document info by ID"""
        return self.documents.get(document_id)
    
    def list_documents(self) -> List[DocumentInfo]:
        """List all documents"""
        return list(self.documents.values())
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document
        
        Args:
            document_id: Document ID
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            if document_id not in self.documents:
                return False
            
            doc_info = self.documents[document_id]
            
            # Delete file
            file_path = self._get_document_path(document_id, doc_info.filename)
            if file_path.exists():
                file_path.unlink()
            
            # Delete from vector store
            if self.vector_store:
                try:
                    self.vector_store.delete_document(document_id)
                except Exception as e:
                    logger.error(f"Error deleting from vector store: {e}")
            
            # Remove from registry
            del self.documents[document_id]
            
            logger.info(f"Document deleted: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False
    
    def _determine_file_type(self, extension: str) -> FileType:
        """Determine file type from extension"""
        ext_map = {
            '.pdf': FileType.PDF,
            '.xlsx': FileType.EXCEL,
            '.xls': FileType.EXCEL,
            '.csv': FileType.CSV
        }
        return ext_map.get(extension.lower(), FileType.PDF)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove any directory separators
        safe_name = Path(filename).name
        # Remove any non-alphanumeric characters except dots, dashes, underscores
        safe_name = "".join(c for c in safe_name if c.isalnum() or c in '.-_')
        return safe_name
    
    def _get_document_path(self, document_id: str, filename: str) -> Path:
        """Get full path to document file"""
        safe_filename = self._sanitize_filename(filename)
        return self.upload_dir / f"{document_id}_{safe_filename}"
    
    def _discover_existing_documents(self):
        """
        Discover and register documents that already exist in upload directory.
        This rebuilds the in-memory registry after restart.
        """
        try:
            logger.info(f"Discovering existing documents in {self.upload_dir}")
            
            # Scan upload directory
            if not self.upload_dir.exists():
                logger.warning(f"Upload directory does not exist: {self.upload_dir}")
                return
            
            discovered_count = 0
            for file_path in self.upload_dir.iterdir():
                if not file_path.is_file():
                    continue
                
                try:
                    # Parse filename: {doc_id}_{original_filename}
                    filename = file_path.name
                    
                    # Split by first underscore to get doc_id
                    parts = filename.split('_', 1)
                    if len(parts) != 2:
                        logger.warning(f"Skipping file with unexpected format: {filename}")
                        continue
                    
                    doc_id = parts[0]
                    original_filename = parts[1]
                    
                    # Validate UUID format
                    try:
                        uuid.UUID(doc_id)
                    except ValueError:
                        logger.warning(f"Skipping file with invalid UUID: {doc_id}")
                        continue
                    
                    # Get file stats
                    file_size = file_path.stat().st_size
                    file_ext = file_path.suffix.lower()
                    file_type = self._determine_file_type(file_ext)
                    
                    # Get modification time as upload time (best approximation)
                    uploaded_at = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    # Create document info
                    doc_info = DocumentInfo(
                        document_id=doc_id,
                        filename=original_filename,
                        file_type=file_type,
                        file_size_bytes=file_size,
                        status=DocumentStatus.PENDING,  # Mark as pending to trigger ingestion
                        uploaded_at=uploaded_at
                    )
                    
                    # Register document
                    self.documents[doc_id] = doc_info
                    discovered_count += 1
                    
                    logger.debug(f"Discovered document: {doc_id} - {original_filename}")
                    
                except Exception as e:
                    logger.error(f"Error processing file {file_path.name}: {e}")
                    continue
            
            logger.info(f"Discovered {discovered_count} existing documents")
            
        except Exception as e:
            logger.error(f"Error discovering existing documents: {e}", exc_info=True)
    
    def _schedule_auto_ingestion(self):
        """
        Schedule auto-ingestion of discovered documents that need processing.
        Only processes documents with PENDING status.
        """
        import threading
        
        def ingest_pending_documents():
            """Background thread to ingest pending documents"""
            try:
                pending_docs = [
                    doc_id for doc_id, doc_info in self.documents.items()
                    if doc_info.status == DocumentStatus.PENDING
                ]
                
                if not pending_docs:
                    logger.info("No pending documents to auto-ingest")
                    return
                
                logger.info(f"Auto-ingesting {len(pending_docs)} pending documents in background")
                
                # Import here to avoid circular imports
                import asyncio
                
                # Create event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                for doc_id in pending_docs:
                    try:
                        logger.info(f"Auto-ingesting document: {doc_id}")
                        loop.run_until_complete(self.ingest_document(doc_id))
                    except Exception as e:
                        logger.error(f"Error auto-ingesting {doc_id}: {e}")
                        continue
                
                loop.close()
                logger.info(f"Auto-ingestion complete: {len(pending_docs)} documents processed")
                
            except Exception as e:
                logger.error(f"Error in auto-ingestion thread: {e}", exc_info=True)
        
        # Start background thread for ingestion
        # Only if there are documents to process
        pending_count = sum(
            1 for doc in self.documents.values() 
            if doc.status == DocumentStatus.PENDING
        )
        
        if pending_count > 0:
            logger.info(f"Starting background auto-ingestion thread for {pending_count} documents")
            thread = threading.Thread(target=ingest_pending_documents, daemon=True)
            thread.start()
        else:
            logger.info("All discovered documents already processed")


# Global service instance
document_service = DocumentService()
