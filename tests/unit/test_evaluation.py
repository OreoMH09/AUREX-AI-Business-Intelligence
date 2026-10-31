"""
Unit tests for Evaluation Metrics
"""
import pytest
from app.evaluation.metrics import EvaluationMetrics, RetrievalMetrics, AnswerMetrics


@pytest.mark.unit
class TestEvaluationMetrics:
    """Test suite for EvaluationMetrics"""
    
    def test_evaluate_retrieval_empty(self):
        """Test retrieval evaluation with no documents"""
        metrics = EvaluationMetrics()
        result = metrics.evaluate_retrieval([])
        
        assert isinstance(result, RetrievalMetrics)
        assert result.num_retrieved == 0
        assert result.avg_similarity == 0.0
    
    def test_evaluate_retrieval_with_docs(self):
        """Test retrieval evaluation with documents"""
        metrics = EvaluationMetrics()
        
        docs = [
            {
                'metadata': {
                    'document_id': 'doc1',
                    'similarity': 0.85
                }
            },
            {
                'metadata': {
                    'document_id': 'doc2',
                    'similarity': 0.75
                }
            }
        ]
        
        result = metrics.evaluate_retrieval(docs)
        
        assert result.num_retrieved == 2
        assert result.avg_similarity > 0
    
    def test_evaluate_retrieval_with_ground_truth(self):
        """Test retrieval evaluation with ground truth"""
        metrics = EvaluationMetrics()
        
        docs = [
            {'metadata': {'document_id': 'doc1', 'similarity': 0.85}},
            {'metadata': {'document_id': 'doc2', 'similarity': 0.75}},
            {'metadata': {'document_id': 'doc3', 'similarity': 0.65}}
        ]
        
        relevant_ids = ['doc1', 'doc3']
        result = metrics.evaluate_retrieval(docs, relevant_ids, k=3)
        
        assert result.precision_at_k > 0
        assert result.recall_at_k > 0
        assert result.mrr > 0
    
    def test_evaluate_answer(self):
        """Test answer evaluation"""
        metrics = EvaluationMetrics()
        
        answer = "The revenue was 450 Lakhs in 2025."
        sources = [{'id': 1}, {'id': 2}]
        latency = 1.5
        
        result = metrics.evaluate_answer(answer, sources, latency)
        
        assert isinstance(result, AnswerMetrics)
        assert result.has_sources is True
        assert result.num_sources == 2
        assert result.contains_numbers is True
        assert result.latency_seconds == 1.5
    
    def test_evaluate_query_complete(self):
        """Test complete query evaluation"""
        metrics = EvaluationMetrics()
        
        query = "What is the revenue?"
        retrieved = [{'metadata': {'document_id': 'doc1', 'similarity': 0.85}}]
        answer = "Revenue is 450 Lakhs"
        sources = [{'id': 1}]
        latency = 2.0
        
        result = metrics.evaluate_query(query, retrieved, answer, sources, latency)
        
        assert result.query == query
        assert result.retrieval is not None
        assert result.answer is not None
        assert len(metrics.results) == 1
    
    def test_get_aggregate_metrics_empty(self):
        """Test aggregate metrics with no data"""
        metrics = EvaluationMetrics()
        result = metrics.get_aggregate_metrics()
        
        assert result['total_queries'] == 0
    
    def test_get_aggregate_metrics_with_data(self):
        """Test aggregate metrics with data"""
        metrics = EvaluationMetrics()
        
        # Add sample evaluations
        for i in range(3):
            metrics.evaluate_query(
                query=f"Query {i}",
                retrieved_docs=[{'metadata': {'similarity': 0.8}}],
                answer="Test answer",
                sources=[{'id': 1}],
                latency=1.0 + i * 0.5
            )
        
        result = metrics.get_aggregate_metrics()
        
        assert result['total_queries'] == 3
        assert 'latency' in result
        assert 'sources' in result
        assert 'answers' in result
    
    def test_clear_results(self):
        """Test clearing results"""
        metrics = EvaluationMetrics()
        
        metrics.evaluate_query("test", [], "answer", [], 1.0)
        assert len(metrics.results) == 1
        
        metrics.clear_results()
        assert len(metrics.results) == 0
