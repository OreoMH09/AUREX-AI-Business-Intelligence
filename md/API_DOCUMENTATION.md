# AUREX API Documentation

Complete API reference for the AUREX Business Intelligence System.

**Base URL**: `http://localhost:8000`  
**Interactive Docs**: `http://localhost:8000/docs`  
**OpenAPI Spec**: `http://localhost:8000/openapi.json`

---

## Table of Contents

- [Authentication](#authentication)
- [Health Endpoints](#health-endpoints)
- [Document Management](#document-management)
- [Query & RAG](#query--rag)
- [Analytics](#analytics)
- [Visualization](#visualization)
- [Reports](#reports)
- [Evaluation](#evaluation)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication. For production deployment, implement:
- API keys
- OAuth 2.0
- JWT tokens

---

## Health Endpoints

### Get System Health

Get overall system health status.

**Endpoint**: `GET /api/health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-09-07T14:30:00.123456",
  "services": {
    "vector_db": "not_configured",
    "llm": "not_configured",
    "embeddings": "not_configured"
  }
}
```

### Get RAG System Health

Check RAG pipeline components.

**Endpoint**: `GET /api/rag-health`

**Response**: `200 OK`
```json
{
  "vector_store": "healthy",
  "llm": "healthy",
  "overall": "healthy",
  "vector_store_chunks": 150
}
```

---

## Document Management

### Upload Document

Upload a business document for ingestion.

**Endpoint**: `POST /api/documents/upload`

**Content-Type**: `multipart/form-data`

**Parameters**:
- `file` (required): Document file (PDF, Excel, CSV)

**Example**:
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@business_report.pdf"
```

**Response**: `200 OK`
```json
{
  "success": true,
  "document_id": "doc_123abc",
  "filename": "business_report.pdf",
  "file_type": "pdf",
  "file_size": 245678,
  "upload_time": "2026-09-07T14:30:00.123456"
}
```

### Ingest Document

Process and index uploaded document.

**Endpoint**: `POST /api/documents/ingest/{document_id}`

**Parameters**:
- `document_id` (path, required): Document ID from upload

**Response**: `200 OK`
```json
{
  "success": true,
  "document_id": "doc_123abc",
  "chunks_created": 25,
  "chunks_indexed": 25,
  "processing_time_ms": 3450
}
```

### List Documents

Get all uploaded documents.

**Endpoint**: `GET /api/documents`

**Response**: `200 OK`
```json
{
  "documents": [
    {
      "document_id": "doc_123abc",
      "filename": "report_2025.pdf",
      "file_type": "pdf",
      "upload_time": "2026-09-07T14:30:00",
      "status": "indexed",
      "chunks": 25
    }
  ],
  "total": 1
}
```

### Get Document

Get details of specific document.

**Endpoint**: `GET /api/documents/{document_id}`

**Response**: `200 OK`
```json
{
  "document_id": "doc_123abc",
  "filename": "report_2025.pdf",
  "file_type": "pdf",
  "file_size": 245678,
  "upload_time": "2026-09-07T14:30:00",
  "status": "indexed",
  "chunks": 25,
  "metadata": {
    "pages": 10,
    "year": 2025
  }
}
```

### Delete Document

Delete document and its embeddings.

**Endpoint**: `DELETE /api/documents/{document_id}`

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Document deleted successfully",
  "document_id": "doc_123abc"
}
```

---

## Query & RAG

### Query RAG System

Ask a question using RAG pipeline.

**Endpoint**: `POST /api/query`

**Request Body**:
```json
{
  "question": "What was the total revenue in 2025?",
  "top_k": 5,
  "document_id": "doc_123abc"  // optional
}
```

**Response**: `200 OK`
```json
{
  "answer": "The total revenue in 2025 was 450 Lakhs according to the business report.",
  "sources": [
    {
      "source_id": 1,
      "document_id": "doc_123abc",
      "chunk_id": "chunk_5",
      "score": 0.87,
      "page_number": 3,
      "content_preview": "Revenue Analysis: Total Revenue: 450 Lakhs..."
    }
  ],
  "retrieved_chunks": 5,
  "processing_time_ms": 3245,
  "timestamp": "2026-09-07T14:30:00.123456"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid question format
- `404 Not Found`: No documents available
- `500 Internal Server Error`: Processing error

---

## Analytics

### Get KPIs

Extract Key Performance Indicators.

**Endpoint**: `GET /api/analytics/kpis`

**Query Parameters**:
- `document_id` (optional): Filter by document

**Response**: `200 OK`
```json
{
  "kpis": {
    "revenue": {
      "value": 450,
      "year": "2025",
      "context": "Total Revenue: 450 Lakhs"
    },
    "profit": {
      "value": 112.5,
      "context": "Profit: 112.5 Lakhs"
    },
    "margin": {
      "value": 25,
      "context": "Profit Margin: 25%"
    },
    "products": [
      {"name": "Widget A", "rank": 1},
      {"name": "Widget B", "rank": 2}
    ],
    "regions": [
      {"name": "North", "rank": 1},
      {"name": "South", "rank": 2}
    ]
  },
  "timestamp": "2026-09-07T14:30:00"
}
```

### Get Summary Statistics

Get aggregated statistics.

**Endpoint**: `GET /api/analytics/summary`

**Response**: `200 OK`
```json
{
  "summary": {
    "total_revenue": 450,
    "total_profit": 112.5,
    "profit_margin": 25,
    "product_count": 3,
    "region_count": 3,
    "time_period": "2025"
  }
}
```

### Get Trends

Analyze trends in data.

**Endpoint**: `GET /api/analytics/trends`

**Response**: `200 OK`
```json
{
  "trends": {
    "revenue_trend": "increasing",
    "quarterly_data": [
      {"period": "Q1", "revenue": 100},
      {"period": "Q2", "revenue": 120}
    ],
    "top_performers": ["Widget A", "Widget B"]
  }
}
```

### Compare Periods

Compare metrics across time periods.

**Endpoint**: `POST /api/analytics/compare`

**Request Body**:
```json
{
  "period1": "2024",
  "period2": "2025",
  "metric": "revenue"
}
```

**Response**: `200 OK`
```json
{
  "comparison": {
    "period1": {
      "name": "2024",
      "value": 400,
      "context": "Revenue 2024: 400 Lakhs"
    },
    "period2": {
      "name": "2025",
      "value": 450,
      "context": "Revenue 2025: 450 Lakhs"
    },
    "change": {
      "absolute": 50,
      "percentage": 12.5,
      "direction": "increase"
    }
  }
}
```

### Year-over-Year Analysis

Analyze year-over-year changes.

**Endpoint**: `POST /api/analytics/yoy`

**Request Body**:
```json
{
  "current_year": "2025",
  "previous_year": "2024",
  "metrics": ["revenue", "profit"]
}
```

**Response**: `200 OK`
```json
{
  "yoy_analysis": {
    "revenue": {
      "current": 450,
      "previous": 400,
      "change_pct": 12.5
    },
    "profit": {
      "current": 112.5,
      "previous": 100,
      "change_pct": 12.5
    }
  }
}
```

### Scenario Analysis

Run what-if scenarios.

**Endpoint**: `POST /api/analytics/scenario`

**Request Body**:
```json
{
  "base_metric": "revenue",
  "change_percentage": 10,
  "scenario_name": "10% Revenue Increase"
}
```

**Response**: `200 OK`
```json
{
  "scenario": {
    "name": "10% Revenue Increase",
    "base_value": 450,
    "new_value": 495,
    "change": 45,
    "impact_assessment": "Positive impact on overall performance",
    "recommendations": [
      "Consider strategies to achieve this growth",
      "Monitor market conditions"
    ]
  }
}
```

### Trend Projection

Project future trends.

**Endpoint**: `POST /api/analytics/projection`

**Request Body**:
```json
{
  "metric": "revenue",
  "periods_ahead": 2,
  "confidence_level": 0.8
}
```

**Response**: `200 OK`
```json
{
  "projection": {
    "metric": "revenue",
    "current_value": 450,
    "projected_values": [
      {"period": "Next Period", "value": 470, "confidence": 0.8},
      {"period": "Period +2", "value": 490, "confidence": 0.7}
    ]
  }
}
```

---

## Visualization

### Create Chart

Generate a visualization chart.

**Endpoint**: `POST /api/visualization/chart`

**Request Body**:
```json
{
  "chart_type": "bar",
  "data": {
    "x": ["Product A", "Product B", "Product C"],
    "y": [100, 150, 120]
  },
  "title": "Product Sales",
  "x_label": "Products",
  "y_label": "Sales (Lakhs)"
}
```

**Chart Types**: `bar`, `line`, `pie`, `scatter`, `area`, `gauge`, `indicator`

**Response**: `200 OK`
```json
{
  "chart": "{...plotly JSON...}",
  "chart_type": "bar",
  "title": "Product Sales"
}
```

### Get KPI Charts

Auto-generate charts from KPI data.

**Endpoint**: `GET /api/visualization/kpi-charts`

**Query Parameters**:
- `document_id` (optional): Filter by document

**Response**: `200 OK`
```json
{
  "charts": [
    {
      "chart": "{...plotly JSON...}",
      "chart_type": "indicator",
      "title": "Total Revenue"
    },
    {
      "chart": "{...plotly JSON...}",
      "chart_type": "bar",
      "title": "Sales by Product"
    }
  ],
  "count": 2
}
```

---

## Reports

### Generate Report

Create a business report.

**Endpoint**: `POST /api/reports/generate`

**Request Body**:
```json
{
  "report_type": "executive",
  "format": "html",
  "document_id": "doc_123abc",
  "title": "Q1 Business Performance"
}
```

**Report Types**: `executive`, `detailed`, `summary`  
**Formats**: `html`, `markdown`, `json`

**Response**: `200 OK`
```json
{
  "success": true,
  "filename": "report_executive_20260907_143000.html",
  "format": "html",
  "report_data": {
    "executive_summary": "Business performance in Q1 2025 shows...",
    "kpis": {...},
    "insights": ["Revenue increased by 12.5%"],
    "recommendations": ["Continue growth strategies"]
  },
  "download_url": "/api/reports/download/report_executive_20260907_143000.html",
  "preview_url": "/api/reports/preview/report_executive_20260907_143000.html"
}
```

### Download Report

Download generated report.

**Endpoint**: `GET /api/reports/download/{filename}`

**Response**: `200 OK`  
Returns file with appropriate Content-Type header.

### Preview Report

Preview HTML report in browser.

**Endpoint**: `GET /api/reports/preview/{filename}`

**Response**: `200 OK`  
Returns HTML content for browser rendering.

---

## Evaluation

### Get Metrics

Get evaluation metrics and statistics.

**Endpoint**: `GET /api/evaluation/metrics`

**Response**: `200 OK`
```json
{
  "success": true,
  "metrics": {
    "total_queries": 25,
    "latency": {
      "avg_seconds": 3.5,
      "min_seconds": 2.1,
      "max_seconds": 5.8
    },
    "sources": {
      "avg_per_query": 4.2,
      "queries_with_sources": 24,
      "percentage_with_sources": 96.0
    },
    "answers": {
      "avg_length_chars": 250,
      "with_numbers": 18
    },
    "retrieval": {
      "avg_similarity_score": 0.78
    }
  }
}
```

### Get Recent Results

Get recent evaluation results.

**Endpoint**: `GET /api/evaluation/results?limit=10`

**Query Parameters**:
- `limit` (optional, default: 10): Number of results

**Response**: `200 OK`
```json
{
  "success": true,
  "count": 10,
  "results": [
    {
      "query": "What was the revenue?",
      "latency": 3.2,
      "num_sources": 4,
      "answer_length": 245,
      "avg_similarity": 0.82,
      "timestamp": 1725712200.123
    }
  ]
}
```

### Clear Evaluation Results

Clear all stored evaluation data.

**Endpoint**: `POST /api/evaluation/clear`

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Evaluation results cleared"
}
```

### Evaluation Health

Check evaluation system status.

**Endpoint**: `GET /api/evaluation/health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "total_evaluations": 25,
  "evaluation_active": true
}
```

---

## Error Handling

### Standard Error Response

All errors return consistent format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "detail": "Additional context (optional)"
}
```

### HTTP Status Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily down

### Example Error Responses

**400 Bad Request**:
```json
{
  "error": "Invalid Input",
  "message": "Question cannot be empty",
  "detail": "The 'question' field is required"
}
```

**404 Not Found**:
```json
{
  "error": "Not Found",
  "message": "Document not found",
  "detail": "Document ID 'doc_invalid' does not exist"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "LLM service unavailable",
  "detail": "Cannot connect to Ollama at localhost:11434"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production:

**Recommended Limits**:
- Query endpoint: 60 requests/minute
- Upload endpoint: 10 requests/minute
- Analytics endpoints: 120 requests/minute

**Implementation**: Use FastAPI middleware or reverse proxy (nginx)

---

## Examples

### Complete Workflow Example

```bash
# 1. Check system health
curl http://localhost:8000/api/health

# 2. Upload document
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@report.pdf"
# Response: {"document_id": "doc_123"}

# 3. Ingest document
curl -X POST "http://localhost:8000/api/documents/ingest/doc_123"

# 4. Query the document
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What was the revenue?"}'

# 5. Get analytics
curl "http://localhost:8000/api/analytics/kpis"

# 6. Generate charts
curl "http://localhost:8000/api/visualization/kpi-charts"

# 7. Create report
curl -X POST "http://localhost:8000/api/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{"report_type": "executive", "format": "html"}'
```

### Python Client Example

```python
import httpx

BASE_URL = "http://localhost:8000"

# Query example
def query_aurex(question: str):
    response = httpx.post(
        f"{BASE_URL}/api/query",
        json={"question": question, "top_k": 5},
        timeout=30.0
    )
    return response.json()

# Upload example
def upload_document(file_path: str):
    with open(file_path, 'rb') as f:
        response = httpx.post(
            f"{BASE_URL}/api/documents/upload",
            files={"file": f}
        )
    return response.json()

# Usage
result = query_aurex("What was the total revenue?")
print(result["answer"])
```

### JavaScript Client Example

```javascript
// Query example
async function queryAurex(question) {
  const response = await fetch('http://localhost:8000/api/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: 5 })
  });
  return await response.json();
}

// Upload example
async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/documents/upload', {
    method: 'POST',
    body: formData
  });
  return await response.json();
}

// Usage
const result = await queryAurex('What was the total revenue?');
console.log(result.answer);
```

---

## Webhooks (Future Enhancement)

Planned webhook support for event notifications:

- `document.uploaded`
- `document.ingested`
- `query.completed`
- `report.generated`

---

## OpenAPI Specification

Full OpenAPI 3.0 specification available at:
- JSON: http://localhost:8000/openapi.json
- Interactive UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## API Versioning

Current version: `v1` (default)

Future versions will use URL prefixing:
- `/api/v1/query`
- `/api/v2/query`

---

## Support

For API questions or issues:
- Interactive docs: http://localhost:8000/docs
- GitHub Issues: [Link to your repo]
- Email: your.email@example.com

---

**Last Updated**: September 2026  
**API Version**: 1.0.0
