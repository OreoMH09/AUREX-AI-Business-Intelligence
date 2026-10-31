# 📊 AUREX - AI Business Intelligence System

**Multimodal RAG-Based Business Intelligence and Decision Support System**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **B.Tech CSE (AIML) Final Year Project** - Production-grade AI system demonstrating advanced software engineering, machine learning, and full-stack development capabilities.

---

## 🎯 Overview

AUREX is an advanced AI-powered Business Intelligence system that transforms raw business documents into actionable insights through natural language queries. Using Retrieval-Augmented Generation (RAG), automated analytics, and interactive visualizations, AUREX enables data-driven decision-making without requiring technical expertise.

### Why AUREX?

- **📄 Multi-Format Support**: PDF, Excel, CSV ingestion with intelligent parsing
- **🤖 Natural Language Interface**: Ask questions in plain English, get AI-powered answers
- **📊 Automated Analytics**: KPI extraction, trend analysis, period comparisons
- **📈 Interactive Visualizations**: Dynamic charts and dashboards with Plotly
- **📑 Professional Reports**: Executive summaries with evidence citations
- **🔍 Evidence-Grounded**: All insights backed by source documents
- **🐋 Production-Ready**: Docker containerization, comprehensive testing, API documentation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AUREX Architecture                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────┐  │
│  │  Streamlit   │───▶│   FastAPI    │───▶│  ChromaDB   │  │
│  │  Frontend    │◀───│   Backend    │◀───│Vector Store │  │
│  │  (Port 8501) │    │  (Port 8000) │    │ (Port 8001) │  │
│  └──────────────┘    └──────────────┘    └─────────────┘  │
│         │                    │                    │         │
│         │                    │                    │         │
│  ┌──────▼────────────────────▼────────────────────▼──────┐ │
│  │              Ollama LLM (llama3.1:8b)                 │ │
│  │                   (Port 11434)                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Components:                                                 │
│  • Document Ingestion (PDF/Excel/CSV)                       │
│  • Vector Embeddings (all-MiniLM-L6-v2)                    │
│  • RAG Query Pipeline                                       │
│  • Analytics Engine (KPI extraction)                        │
│  • Visualization Engine (Plotly charts)                     │
│  • Report Generator (HTML/Markdown/JSON)                    │
│  • Evaluation Framework (metrics tracking)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Ollama with llama3.1:8b model
- 8GB RAM minimum
- Windows/Linux/Mac

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AUREX.git
cd AUREX
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install and start Ollama:**
```bash
# Download from https://ollama.ai
ollama pull llama3.1:8b
ollama serve
```

5. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

6. **Start the application:**
```bash
# Windows
START_AUREX.bat

# Linux/Mac
./start_aurex.sh
```

7. **Access the application:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🐋 Docker Deployment

### Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Ports:**
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- ChromaDB: http://localhost:8001

See [DOCKER.md](DOCKER.md) for detailed deployment guide.

---

## 📖 Usage Guide

### 1. Upload Documents

Navigate to the **Upload** page and upload your business documents:
- **PDF**: Financial reports, invoices, contracts
- **Excel**: Sales data, financial statements, inventory
- **CSV**: Transaction logs, customer data, metrics

### 2. Ask Questions

Go to the **AI Business Analyst** page and ask questions:

**Example Questions:**
- "What was the total revenue in 2025?"
- "Which product generated the highest profit?"
- "Compare revenue between Q1 and Q2"
- "What are the top 3 regions by sales?"
- "What was the profit margin last year?"

### 3. View Dashboard

Visit the **Dashboard** page for:
- Live KPI cards (revenue, profit, margin)
- Automated charts (revenue trends, product distribution)
- Interactive visualizations
- Real-time metrics

### 4. Generate Reports

Use the **Reports** page to:
- Select report type (Executive, Detailed, Summary)
- Choose format (HTML, Markdown, JSON)
- Generate professional business reports
- Download or preview in browser

---

## 🎨 Features in Detail

### Multi-Format Document Ingestion

**PDF Processing:**
- Text extraction with PyMuPDF
- Table parsing and structure preservation
- Metadata capture (filename, page numbers, dates)
- Section/heading detection
- OCR support for scanned documents

**Excel Processing:**
- Multi-sheet handling
- Data type detection (numeric, date, text)
- Business field identification (revenue, costs, dates)
- Header and row-level metadata
- Chunk-based processing for large files

**CSV Processing:**
- Automatic delimiter detection
- Schema inference
- UTF-8 encoding with fallback
- Streaming for large datasets

### RAG Pipeline

**Vector Store (ChromaDB):**
- 384-dimensional embeddings (all-MiniLM-L6-v2)
- Persistent storage
- Similarity-based retrieval
- Metadata filtering

**Query Engine:**
- Semantic search with configurable similarity threshold
- Top-K document retrieval
- Context assembly with source tracking
- LLM-based answer generation
- Citation tracking with page/sheet references

### Analytics Engine

**Automated KPI Extraction:**
- Revenue, profit, margin calculations
- Product and region identification
- Trend analysis
- Growth rate calculations
- Ranking and sorting

**Advanced Analytics:**
- **Period Comparison**: Month-over-month, Year-over-year
- **Scenario Analysis**: What-if simulations with percentage changes
- **Trend Projection**: Future value predictions with confidence levels
- **Impact Assessment**: Change calculations and recommendations

### Visualization Engine

**Chart Types:**
- Bar charts (product/region performance)
- Line charts (trends over time)
- Pie charts (distribution analysis)
- Gauge charts (KPI indicators)
- Indicator cards (single metrics)
- Scatter plots (correlation analysis)
- Area charts (cumulative metrics)

**Features:**
- Interactive Plotly charts
- Zoom, pan, hover tooltips
- JSON serialization for API
- Automated chart generation from KPI data
- Responsive layouts

### Report Generator

**Report Types:**
- **Executive**: High-level summary with key insights
- **Detailed**: Comprehensive analysis with all metrics
- **Summary**: Quick overview of essential KPIs

**Output Formats:**
- **HTML**: Formatted with styling and charts
- **Markdown**: Clean text with structure
- **JSON**: Structured data for integration

**Content:**
- Executive summary
- KPI cards with values and changes
- Key insights and findings
- Evidence-based recommendations
- Source citations

### Evaluation Framework

**Metrics Tracked:**
- **Retrieval Quality**: Precision@K, Recall@K, MRR, similarity scores
- **Answer Quality**: Source count, length, numerical content
- **Latency**: Query processing time, end-to-end latency
- **Aggregate Stats**: Average metrics across all queries

**API Endpoints:**
- `/api/evaluation/metrics` - Get aggregate statistics
- `/api/evaluation/results` - Recent evaluation results
- `/api/evaluation/health` - System health check

---

## 🔌 API Documentation

### Core Endpoints

#### Health Check
```http
GET /api/health
```
Returns system status and version information.

#### Document Upload
```http
POST /api/documents/upload
Content-Type: multipart/form-data

file: <document_file>
```

#### Query
```http
POST /api/query
Content-Type: application/json

{
  "question": "What was the total revenue?",
  "top_k": 5
}
```

#### Analytics - Get KPIs
```http
GET /api/analytics/kpis?document_id=optional
```

#### Visualization - Generate Chart
```http
POST /api/visualization/chart
Content-Type: application/json

{
  "chart_type": "bar",
  "data": {"x": [...], "y": [...]},
  "title": "Sales by Product"
}
```

#### Reports - Generate
```http
POST /api/reports/generate
Content-Type: application/json

{
  "report_type": "executive",
  "format": "html"
}
```

**Full API documentation**: http://localhost:8000/docs

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests -v
```

### Run Specific Test Types
```bash
# Unit tests
pytest tests/unit -m unit -v

# Integration tests
pytest tests/integration -m integration -v

# End-to-end tests
pytest tests/e2e -m e2e -v

# Fast tests (skip slow E2E)
pytest tests -m "not slow" -v
```

### Using Test Runner (Windows)
```bash
run_tests.bat          # All tests
run_tests.bat unit     # Unit only
run_tests.bat fast     # Quick validation
```

**Test Coverage:**
- Unit tests: Analytics, Evaluation, Visualization
- Integration tests: API endpoints, health checks
- E2E tests: Complete workflows (RAG, analytics, reports)

See [tests/README.md](tests/README.md) for detailed testing guide.

---

## 📁 Project Structure

```
AUREX/
├── app/                          # Backend application
│   ├── api/                      # API routes
│   │   └── routes/               # Endpoint definitions
│   ├── ingestion/                # Document parsers
│   │   ├── pdf_parser.py
│   │   ├── excel_parser.py
│   │   └── csv_parser.py
│   ├── vector_store/             # ChromaDB integration
│   ├── llm/                      # Ollama client
│   ├── rag/                      # RAG pipeline
│   ├── analytics/                # Analytics engine
│   │   ├── engine.py
│   │   └── advanced.py
│   ├── visualization/            # Plotly charts
│   ├── reports/                  # Report generator
│   ├── evaluation/               # Metrics framework
│   └── main.py                   # FastAPI app
├── frontend/                     # Streamlit UI
│   ├── pages/                    # UI pages
│   │   ├── 1_📤_Upload.py
│   │   ├── 2_🤖_AI_Business_Analyst.py
│   │   ├── 3_📊_Dashboard.py
│   │   └── 4_📄_Reports.py
│   └── streamlit_app.py          # Main app
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # E2E tests
├── data/                         # Data storage
│   ├── uploads/                  # Uploaded documents
│   ├── chroma_db/                # Vector database
│   ├── reports/                  # Generated reports
│   └── sample/                   # Sample data
├── docker-compose.yml            # Production deployment
├── docker-compose.dev.yml        # Development deployment
├── Dockerfile                    # Container image
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Test configuration
├── .env.example                  # Environment template
├── START_AUREX.bat              # Windows launcher
├── run_tests.bat                # Test runner
├── README.md                     # This file
├── DOCKER.md                     # Docker guide
└── PROJECT_TRACKER.md            # Development log
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python 3.11**: Latest stable Python

### AI/ML
- **Ollama**: Local LLM hosting (llama3.1:8b)
- **ChromaDB**: Vector database
- **Sentence Transformers**: Embeddings (all-MiniLM-L6-v2)
- **PyMuPDF (fitz)**: PDF processing
- **openpyxl**: Excel processing
- **pandas**: Data manipulation

### Visualization & Reports
- **Plotly**: Interactive charts
- **Kaleido**: Chart export
- **Jinja2**: Template rendering (for HTML reports)

### Frontend
- **Streamlit**: Rapid UI development
- **httpx**: Async HTTP client

### Development & Testing
- **pytest**: Testing framework
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Ollama Configuration
OLLAMA_HOST=127.0.0.1
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.1:8b

# Vector Store
CHROMA_PERSIST_DIR=data/chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# RAG Settings
TOP_K=5
SIMILARITY_THRESHOLD=0.3

# Storage
UPLOAD_DIR=data/uploads
REPORTS_DIR=data/reports

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

---

## 📊 Performance

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 10GB
- GPU: Not required (CPU inference)

**Recommended:**
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 50GB SSD
- GPU: Optional (faster inference)

### Benchmarks

**Query Performance:**
- Document retrieval: ~200-500ms
- LLM generation: ~2-5s (depends on answer length)
- Total query time: ~3-6s average

**Ingestion:**
- PDF (10 pages): ~5-10s
- Excel (1000 rows): ~3-5s
- CSV (10K rows): ~10-15s

**Analytics:**
- KPI extraction: ~5-10s
- Chart generation: ~1-2s
- Report generation: ~15-30s

---

## 🔐 Security Considerations

- **Input Validation**: All inputs validated with Pydantic
- **File Type Checking**: Strict file type validation
- **Path Traversal Protection**: Secure file handling
- **Error Handling**: Graceful error messages without exposing internals
- **CORS**: Configurable for production deployment
- **Environment Variables**: Sensitive data in .env
- **Docker**: Network isolation between services

**Production Recommendations:**
- Use HTTPS for API endpoints
- Implement authentication/authorization
- Rate limiting on API endpoints
- Regular security updates
- Monitor logs for suspicious activity

---

## 🐛 Troubleshooting

### Common Issues

**1. Ollama Connection Error**
```
Solution: Ensure Ollama is running
- Check: curl http://localhost:11434/api/tags
- Start: ollama serve
```

**2. ChromaDB Not Found**
```
Solution: Initialize vector database
- Backend will auto-create on first run
- Check: data/chroma_db directory exists
```

**3. Port Already in Use**
```
Solution: Change ports in .env
- API_PORT=8000 → 8002
- Or stop conflicting process
```

**4. Out of Memory**
```
Solution: Reduce batch sizes or upgrade RAM
- Adjust TOP_K in .env (lower = less memory)
- Process smaller documents
```

**5. Slow Queries**
```
Solution: Optimize configuration
- Reduce TOP_K to 3-5
- Use faster embedding model
- Ensure Ollama is using GPU if available
```

---

## 📈 Roadmap

### Completed ✅
- Multi-format document ingestion (PDF, Excel, CSV)
- Vector database with semantic search
- RAG pipeline with source citations
- Automated analytics and KPI extraction
- Interactive visualizations with Plotly
- Professional report generation
- Advanced analytics (comparison, scenarios, trends)
- Evaluation framework
- Comprehensive testing
- Docker containerization
- Complete documentation

### Future Enhancements 🚀
- Real-time data streaming
- Multi-language support
- Advanced NLP (named entity recognition, sentiment analysis)
- Custom visualization templates
- Collaborative features (user annotations, shared reports)
- API authentication and rate limiting
- Cloud deployment (AWS, Azure, GCP)
- Mobile responsive UI
- Email report delivery
- Scheduled report generation

---

## 🤝 Contributing

This is an academic project (B.Tech final year). Contributions, suggestions, and feedback are welcome!

### Development Setup

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Install dev dependencies: `pip install -r requirements-dev.txt`
4. Make changes and test: `pytest tests -v`
5. Commit changes (`git commit -m 'Add AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Your Name**
- B.Tech CSE (AIML) - Final Year Project
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Ollama Team**: For providing excellent local LLM infrastructure
- **FastAPI**: For the modern, fast web framework
- **Streamlit**: For rapid UI development
- **ChromaDB**: For the vector database
- **Hugging Face**: For pre-trained models
- **My College/University**: For project guidance and support
- **Open Source Community**: For all the amazing tools

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AUREX/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AUREX/discussions)
- **Email**: your.email@example.com

---

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Docker Deployment Guide](DOCKER.md)
- [Testing Guide](tests/README.md)
- [Project Tracker](PROJECT_TRACKER.md)

---

<p align="center">
  <strong>Built with ❤️ for the future of AI-powered business intelligence</strong>
</p>

<p align="center">
  <sub>AUREX - Transforming Data into Decisions</sub>
</p>
