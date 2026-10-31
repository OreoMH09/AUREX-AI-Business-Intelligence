"""
AUREX Embeddings Service
Generates embeddings for text using sentence transformers
"""
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core import settings, get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize embedding service
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name or settings.embedding_model
        self.dimension = settings.embedding_dimension
        
        logger.info(f"Loading embedding model: {self.model_name}")
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model loaded successfully (dimension: {self.dimension})")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return [0.0] * self.dimension
            
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing)
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            
        Returns:
            List of embedding vectors
        """
        try:
            if not texts:
                logger.warning("Empty text list provided for batch embedding")
                return []
            
            # Filter out empty texts
            valid_texts = [t if t and t.strip() else " " for t in texts]
            
            logger.info(f"Generating embeddings for {len(valid_texts)} texts")
            
            embeddings = self.model.encode(
                valid_texts,
                batch_size=batch_size,
                show_progress_bar=len(valid_texts) > 100,
                convert_to_numpy=True
            )
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Cosine similarity
            similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0


# Global embedding service instance
embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create global embedding service instance"""
    global embedding_service
    if embedding_service is None:
        embedding_service = EmbeddingService()
    return embedding_service
