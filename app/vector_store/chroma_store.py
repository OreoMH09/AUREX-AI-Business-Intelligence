"""
AUREX ChromaDB Vector Store
Manages document embeddings and similarity search
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
import uuid

from app.ingestion.base import DocumentChunk
from app.vector_store.embeddings import get_embedding_service
from app.core import settings, get_logger

logger = get_logger(__name__)


class ChromaVectorStore:
    """ChromaDB vector store for document embeddings"""
    
    def __init__(self):
        """Initialize ChromaDB vector store"""
        self.persist_dir = Path(settings.chroma_persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        self.collection_name = settings.collection_name
        self.embedding_service = get_embedding_service()
        
        logger.info(f"Initializing ChromaDB at: {self.persist_dir}")
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "AUREX document embeddings"}
            )
            
            logger.info(f"ChromaDB initialized: collection '{self.collection_name}'")
            logger.info(f"Current collection size: {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise
    
    def add_documents(
        self,
        chunks: List[DocumentChunk],
        document_id: str,
        batch_size: int = 100
    ) -> int:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of document chunks
            document_id: Parent document ID
            batch_size: Batch size for processing
            
        Returns:
            Number of chunks added
        """
        try:
            if not chunks:
                logger.warning("No chunks provided to add")
                return 0
            
            logger.info(f"Adding {len(chunks)} chunks for document {document_id}")
            
            # Prepare data for batch insertion
            ids = []
            documents = []
            metadatas = []
            
            for chunk in chunks:
                # Generate unique ID for chunk
                chunk_id = f"{document_id}_{chunk.chunk_id}"
                
                # Prepare metadata
                metadata = {
                    "document_id": document_id,
                    "chunk_id": chunk.chunk_id,
                    "page_number": chunk.page_number or 0,
                    **(chunk.metadata or {})
                }
                
                # Convert all metadata values to strings (ChromaDB requirement)
                metadata = {k: str(v) for k, v in metadata.items()}
                
                ids.append(chunk_id)
                documents.append(chunk.content)
                metadatas.append(metadata)
            
            # Generate embeddings in batches
            logger.info(f"Generating embeddings for {len(documents)} chunks")
            embeddings = self.embedding_service.embed_batch(documents, batch_size=batch_size)
            
            # Add to ChromaDB in batches
            for i in range(0, len(ids), batch_size):
                batch_end = min(i + batch_size, len(ids))
                
                self.collection.add(
                    ids=ids[i:batch_end],
                    documents=documents[i:batch_end],
                    embeddings=embeddings[i:batch_end],
                    metadatas=metadatas[i:batch_end]
                )
            
            logger.info(f"Successfully added {len(chunks)} chunks to vector store")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}", exc_info=True)
            raise
    
    def search(
        self,
        query: str,
        top_k: int = None,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_dict: Metadata filters
            
        Returns:
            List of search results with content and metadata
        """
        try:
            top_k = top_k or settings.top_k
            
            logger.info(f"Searching vector store: query='{query[:50]}...', top_k={top_k}")
            
            # Generate query embedding
            query_embedding = self.embedding_service.embed_text(query)
            
            # Search ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_dict
            )
            
            # Format results
            formatted_results = []
            
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    result = {
                        'id': results['ids'][0][i],
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None,
                        'score': 1 - results['distances'][0][i] if 'distances' in results else None
                    }
                    formatted_results.append(result)
            
            logger.info(f"Found {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}", exc_info=True)
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete all chunks for a document
        
        Args:
            document_id: Document ID to delete
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Deleting document {document_id} from vector store")
            
            # Query for all chunks with this document_id
            results = self.collection.get(
                where={"document_id": document_id}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document from vector store: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get vector store statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            count = self.collection.count()
            
            return {
                "collection_name": self.collection_name,
                "total_chunks": count,
                "persist_dir": str(self.persist_dir)
            }
            
        except Exception as e:
            logger.error(f"Error getting vector store stats: {e}")
            return {}
    
    def reset(self):
        """Reset/clear the vector store (use with caution!)"""
        try:
            logger.warning("Resetting vector store - all data will be deleted!")
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "AUREX document embeddings"}
            )
            logger.info("Vector store reset complete")
            
        except Exception as e:
            logger.error(f"Error resetting vector store: {e}")
            raise


# Global vector store instance
vector_store = None


def get_vector_store() -> ChromaVectorStore:
    """Get or create global vector store instance"""
    global vector_store
    if vector_store is None:
        vector_store = ChromaVectorStore()
    return vector_store
