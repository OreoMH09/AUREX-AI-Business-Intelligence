"""
Evaluation metrics for RAG system performance
Measures retrieval quality, answer accuracy, and system latency
"""
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re

logger = logging.getLogger("aurex.evaluation")


@dataclass
class RetrievalMetrics:
    """Metrics for document retrieval quality"""
    precision_at_k: float
    recall_at_k: float
    mrr: float  # Mean Reciprocal Rank
    avg_similarity: float
    num_retrieved: int


@dataclass
class AnswerMetrics:
    """Metrics for answer quality"""
    has_sources: bool
    num_sources: int
    answer_length: int
    contains_numbers: bool
    latency_seconds: float


@dataclass
class EvaluationResult:
    """Complete evaluation result"""
    query: str
    retrieval: Optional[RetrievalMetrics]
    answer: AnswerMetrics
    timestamp: float


class EvaluationMetrics:
    """
    Evaluation framework for AUREX RAG system
    Measures retrieval quality, answer accuracy, and latency
    """
    
    def __init__(self):
        """Initialize evaluation metrics"""
        self.results: List[EvaluationResult] = []
        logger.info("EvaluationMetrics initialized")
    
    def evaluate_retrieval(
        self,
        retrieved_docs: List[Dict[str, Any]],
        relevant_doc_ids: Optional[List[str]] = None,
        k: int = 5
    ) -> RetrievalMetrics:
        """
        Evaluate retrieval quality
        
        Args:
            retrieved_docs: List of retrieved documents with metadata
            relevant_doc_ids: List of known relevant document IDs (if available)
            k: Number of top documents to consider
        
        Returns:
            RetrievalMetrics with precision, recall, MRR, avg similarity
        """
        if not retrieved_docs:
            return RetrievalMetrics(
                precision_at_k=0.0,
                recall_at_k=0.0,
                mrr=0.0,
                avg_similarity=0.0,
                num_retrieved=0
            )
        
        # Calculate average similarity score
        similarities = [
            doc.get('metadata', {}).get('similarity', 0.0)
            for doc in retrieved_docs[:k]
        ]
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
        
        # If we have ground truth relevant docs, calculate precision/recall
        precision = 0.0
        recall = 0.0
        mrr = 0.0
        
        if relevant_doc_ids:
            retrieved_ids = [
                doc.get('metadata', {}).get('document_id')
                for doc in retrieved_docs[:k]
            ]
            
            # Precision@K: % of retrieved docs that are relevant
            relevant_retrieved = sum(
                1 for doc_id in retrieved_ids if doc_id in relevant_doc_ids
            )
            precision = relevant_retrieved / k if k > 0 else 0.0
            
            # Recall@K: % of relevant docs that were retrieved
            recall = relevant_retrieved / len(relevant_doc_ids) if relevant_doc_ids else 0.0
            
            # MRR: Mean Reciprocal Rank
            for idx, doc_id in enumerate(retrieved_ids, 1):
                if doc_id in relevant_doc_ids:
                    mrr = 1.0 / idx
                    break
        
        return RetrievalMetrics(
            precision_at_k=precision,
            recall_at_k=recall,
            mrr=mrr,
            avg_similarity=avg_similarity,
            num_retrieved=len(retrieved_docs)
        )
    
    def evaluate_answer(
        self,
        answer: str,
        sources: List[Dict[str, Any]],
        latency: float
    ) -> AnswerMetrics:
        """
        Evaluate answer quality
        
        Args:
            answer: Generated answer text
            sources: List of source documents used
            latency: Time taken to generate answer (seconds)
        
        Returns:
            AnswerMetrics with quality indicators
        """
        # Check if answer contains numerical values
        contains_numbers = bool(re.search(r'\d+', answer))
        
        return AnswerMetrics(
            has_sources=len(sources) > 0,
            num_sources=len(sources),
            answer_length=len(answer),
            contains_numbers=contains_numbers,
            latency_seconds=round(latency, 3)
        )
    
    def evaluate_query(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        answer: str,
        sources: List[Dict[str, Any]],
        latency: float,
        relevant_doc_ids: Optional[List[str]] = None
    ) -> EvaluationResult:
        """
        Complete evaluation for a single query
        
        Args:
            query: User query
            retrieved_docs: Retrieved documents from vector store
            answer: Generated answer
            sources: Source documents cited
            latency: Total query latency
            relevant_doc_ids: Ground truth relevant docs (optional)
        
        Returns:
            EvaluationResult with all metrics
        """
        retrieval_metrics = None
        if retrieved_docs:
            retrieval_metrics = self.evaluate_retrieval(
                retrieved_docs,
                relevant_doc_ids
            )
        
        answer_metrics = self.evaluate_answer(answer, sources, latency)
        
        result = EvaluationResult(
            query=query,
            retrieval=retrieval_metrics,
            answer=answer_metrics,
            timestamp=time.time()
        )
        
        self.results.append(result)
        
        logger.info(
            f"Evaluated query: latency={latency:.3f}s, "
            f"sources={len(sources)}, "
            f"avg_similarity={retrieval_metrics.avg_similarity if retrieval_metrics else 0:.3f}"
        )
        
        return result
    
    def get_aggregate_metrics(self) -> Dict[str, Any]:
        """
        Calculate aggregate metrics across all evaluations
        
        Returns:
            Dictionary with aggregate statistics
        """
        if not self.results:
            return {
                "total_queries": 0,
                "message": "No evaluations performed yet"
            }
        
        # Latency statistics
        latencies = [r.answer.latency_seconds for r in self.results]
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        
        # Source statistics
        avg_sources = sum(r.answer.num_sources for r in self.results) / len(self.results)
        queries_with_sources = sum(1 for r in self.results if r.answer.has_sources)
        
        # Answer length statistics
        avg_length = sum(r.answer.answer_length for r in self.results) / len(self.results)
        
        # Retrieval statistics (if available)
        retrieval_results = [r.retrieval for r in self.results if r.retrieval]
        avg_similarity = 0.0
        if retrieval_results:
            avg_similarity = sum(
                r.avg_similarity for r in retrieval_results
            ) / len(retrieval_results)
        
        return {
            "total_queries": len(self.results),
            "latency": {
                "avg_seconds": round(avg_latency, 3),
                "min_seconds": round(min_latency, 3),
                "max_seconds": round(max_latency, 3)
            },
            "sources": {
                "avg_per_query": round(avg_sources, 2),
                "queries_with_sources": queries_with_sources,
                "percentage_with_sources": round(queries_with_sources / len(self.results) * 100, 1)
            },
            "answers": {
                "avg_length_chars": round(avg_length, 0),
                "with_numbers": sum(1 for r in self.results if r.answer.contains_numbers)
            },
            "retrieval": {
                "avg_similarity_score": round(avg_similarity, 3)
            }
        }
    
    def get_latest_results(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get the N most recent evaluation results
        
        Args:
            n: Number of recent results to return
        
        Returns:
            List of result dictionaries
        """
        recent = self.results[-n:] if len(self.results) > n else self.results
        
        return [
            {
                "query": r.query,
                "latency": r.answer.latency_seconds,
                "num_sources": r.answer.num_sources,
                "answer_length": r.answer.answer_length,
                "avg_similarity": r.retrieval.avg_similarity if r.retrieval else 0.0,
                "timestamp": r.timestamp
            }
            for r in recent
        ]
    
    def clear_results(self):
        """Clear all evaluation results"""
        self.results.clear()
        logger.info("Evaluation results cleared")


# Global instance
_evaluation_metrics: Optional[EvaluationMetrics] = None


def get_evaluation_metrics() -> EvaluationMetrics:
    """Get or create global evaluation metrics instance"""
    global _evaluation_metrics
    if _evaluation_metrics is None:
        _evaluation_metrics = EvaluationMetrics()
    return _evaluation_metrics
