"""
AUREX RAG Query Engine
Combines retrieval and generation for question answering
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from app.vector_store.chroma_store import get_vector_store
from app.llm.client import get_llm_client
from app.llm.prompts import BUSINESS_ANALYST_SYSTEM_PROMPT, build_rag_prompt
from app.evaluation import get_evaluation_metrics
from app.core import settings, get_logger

logger = get_logger(__name__)


class QueryEngine:
    """RAG Query Engine for document-based question answering"""
    
    def __init__(self):
        """Initialize query engine"""
        try:
            self.vector_store = get_vector_store()
        except Exception as e:
            logger.warning(f"Vector store initialization failed, will work without it: {e}")
            self.vector_store = None
        
        self.llm_client = get_llm_client()
        self.evaluation_metrics = get_evaluation_metrics()
        self.chart_engine = None  # Lazy initialization to avoid circular import
        self.top_k = settings.top_k
        self.similarity_threshold = settings.similarity_threshold
        
        logger.info("QueryEngine initialized with evaluation metrics and chart engine")
    
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        document_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG
        
        Args:
            question: User question
            top_k: Number of documents to retrieve
            document_filter: Filter by document ID
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            logger.info(f"Processing query: {question}")
            start_time = time.time()
            
            # NO CHART GENERATION - Just answer the question with RAG
            
            # Step 1: Retrieve relevant documents
            top_k = top_k or self.top_k
            
            filter_dict = None
            if document_filter:
                filter_dict = {"document_id": document_filter}
            
            # Check if vector store is available
            if self.vector_store is None:
                logger.warning("Vector store not available, returning minimal response")
                return {
                    "answer": "Vector database is currently unavailable. Please use the Dashboard or Reports pages for visualizations.",
                    "sources": [],
                    "retrieved_chunks": 0,
                    "processing_time_ms": int((time.time() - start_time) * 1000)
                }
            
            logger.info(f"Retrieving top {top_k} documents")
            retrieved_docs = self.vector_store.search(
                query=question,
                top_k=top_k,
                filter_dict=filter_dict
            )
            
            if not retrieved_docs:
                logger.warning("No documents retrieved")
                return {
                    "answer": "I don't have enough information to answer this question. Please upload relevant documents first.",
                    "sources": [],
                    "retrieved_chunks": 0,
                    "processing_time_ms": 0
                }
            
            # Step 2: Filter by similarity threshold
            filtered_docs = [
                doc for doc in retrieved_docs
                if doc.get('score', 0) >= self.similarity_threshold
            ]
            
            if not filtered_docs:
                logger.warning(f"No documents met similarity threshold {self.similarity_threshold}")
                filtered_docs = retrieved_docs[:3]  # Use top 3 anyway
            
            logger.info(f"Retrieved {len(filtered_docs)} relevant chunks")
            
            # Step 3: Build context from retrieved documents
            context = self._build_context(filtered_docs)
            
            # Step 4: Generate answer using LLM - PROPER COMPLETE ANSWER
            logger.info("Generating complete answer with LLM")
            prompt = build_rag_prompt(context=context, question=question)
            
            answer = self.llm_client.generate(
                prompt=prompt,
                system_prompt=BUSINESS_ANALYST_SYSTEM_PROMPT,
                stream=False
            )
            
            # Step 5: Format response
            end_time = time.time()
            latency_seconds = end_time - start_time
            processing_time_ms = int(latency_seconds * 1000)
            
            sources = self._format_sources(filtered_docs)
            
            # Step 6: Evaluate query performance
            try:
                # Format retrieved docs for evaluation
                retrieved_for_eval = [
                    {
                        'metadata': {
                            'document_id': doc.get('metadata', {}).get('document_id'),
                            'similarity': doc.get('score', 0)
                        }
                    }
                    for doc in retrieved_docs
                ]
                
                self.evaluation_metrics.evaluate_query(
                    query=question,
                    retrieved_docs=retrieved_for_eval,
                    answer=answer.strip(),
                    sources=sources,
                    latency=latency_seconds
                )
            except Exception as eval_err:
                logger.warning(f"Evaluation failed: {eval_err}")
            
            # Combine chart explanation with LLM answer if needed
            final_answer = answer.strip()
            
            result = {
                "answer": final_answer,
                "sources": sources,
                "retrieved_chunks": len(filtered_docs),
                "processing_time_ms": processing_time_ms,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Query processed successfully in {processing_time_ms}ms")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "retrieved_chunks": 0,
                "processing_time_ms": 0,
                "error": str(e)
            }
    
    def _build_context(self, documents: List[Dict[str, Any]], max_chars: int = 4000) -> str:
        """
        Build context string from retrieved documents
        
        Args:
            documents: List of retrieved documents
            max_chars: Maximum context length
            
        Returns:
            Context string
        """
        context_parts = []
        total_chars = 0
        
        for i, doc in enumerate(documents):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            score = doc.get('score', 0)
            
            # Format source reference
            source_ref = f"[Source {i+1}]"
            if 'document_id' in metadata:
                source_ref += f" (Document: {metadata['document_id']}"
                if 'page_number' in metadata:
                    source_ref += f", Page: {metadata['page_number']}"
                source_ref += ")"
            
            chunk_text = f"{source_ref}\n{content}\n"
            
            # Check if adding this would exceed max length
            if total_chars + len(chunk_text) > max_chars:
                break
            
            context_parts.append(chunk_text)
            total_chars += len(chunk_text)
        
        return "\n---\n".join(context_parts)
    
    def _format_sources(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format source references for response
        
        Args:
            documents: Retrieved documents
            
        Returns:
            List of formatted sources
        """
        sources = []
        
        for i, doc in enumerate(documents):
            metadata = doc.get('metadata', {})
            
            source = {
                "source_id": i + 1,
                "document_id": metadata.get('document_id', 'unknown'),
                "chunk_id": metadata.get('chunk_id', 'unknown'),
                "score": round(doc.get('score', 0), 3),
                "page_number": metadata.get('page_number'),
                "content_preview": doc.get('content', '')[:200] + "..."
            }
            
            sources.append(source)
        
        return sources
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check health of RAG components
        
        Returns:
            Health status dictionary
        """
        health = {
            "vector_store": "unknown",
            "llm": "unknown",
            "overall": "unhealthy"
        }
        
        try:
            # Check vector store
            if self.vector_store:
                stats = self.vector_store.get_stats()
                if stats:
                    health["vector_store"] = "healthy"
                    health["vector_store_chunks"] = stats.get("total_chunks", 0)
            else:
                health["vector_store"] = "unavailable"
        except Exception as e:
            logger.error(f"Vector store health check failed: {e}")
            health["vector_store"] = "unhealthy"
        
        try:
            # Check LLM
            if self.llm_client.check_health():
                health["llm"] = "healthy"
            else:
                health["llm"] = "unhealthy"
        except Exception as e:
            logger.error(f"LLM health check failed: {e}")
            health["llm"] = "unhealthy"
        
        # Overall health
        if health["vector_store"] == "healthy" and health["llm"] == "healthy":
            health["overall"] = "healthy"
        
        return health


# Global query engine instance
query_engine = None


def get_query_engine() -> QueryEngine:
    """Get or create global query engine instance"""
    global query_engine
    if query_engine is None:
        query_engine = QueryEngine()
    return query_engine
