# 🚀 AUREX - AI Business Intelligence System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AUREX** (Automated Universal RAG-Enhanced eXplorer) is an advanced AI-powered business intelligence system that combines **Retrieval-Augmented Generation (RAG)**, **Natural Language Processing**, and **Automated Analytics** to transform business documents into actionable insights.

---

## ✨ Key Features

### 🤖 **AI-Powered Query Engine**
- Natural language question answering using RAG architecture
- Multi-document semantic search with ChromaDB vector database
- Context-aware responses with source citations
- Sub-2 second query response time using Groq API

### 📊 **Automated Business Analytics**
- Intelligent KPI extraction from business documents
- Trend analysis and pattern detection
- Product and regional performance insights
- Automated profitability analysis

### 📄 **Smart Report Generation**
- Executive, Detailed, and Summary report types
- AI-generated insights and recommendations
- Multiple export formats (HTML, Markdown, JSON)
- Professional report templates with data visualization

### 📈 **Interactive Dashboard**
- Real-time business metrics visualization
- Upload and process multiple document types (CSV, PDF, Excel, TXT)
- Document management interface
- Health monitoring and status tracking

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Streamlit)                     │
│  ┌─────────┬──────────────┬──────────┬───────────────────┐ │
│  │Dashboard│ AI Assistant │ Upload   │ Reports           │ │
│  └─────────┴──────────────┴──────────┴───────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────┴────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┬─────────────┬──────────────────────────┐ │
│  │ Query Engine │ Analytics   │ Report Generator         │ │
│  │ (RAG)        │ Engine      │                          │ │
│  └──────────────┴─────────────┴──────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴───────────────┬─────────────────┐
          │                              │                 │
    ┌─────▼──────┐              ┌───────▼──────┐   ┌──────▼──────┐
    │ ChromaDB   │              │  Groq API    │   │ File System │
    │ Vector DB  │              │  LLM         │   │ Documents   │
    └────────────┘              └──────────────┘   └─────────────┘
```

### **Core Components:**

#### **1. RAG Pipeline**
- **Document Processor**: Handles CSV, PDF, DOCX, TXT files
- **Embeddings**: Sentence Transformers for semantic search
- **Vector Store**: ChromaDB with 339+ document chunks
- **LLM**: Groq API (openai/gpt-oss-120b model)
- **Query Engine**: Context retrieval + answer generation

#### **2. Multi-Agent System**
- **Query Agent**: Natural language question answering
- **Analytics Agent**: Automated EDA and KPI extraction
- **Report Agent**: Comprehensive report generation

#### **3. Analytics Engine**
- Statistical analysis (mean, sum, percentages)
- Trend detection and pattern recognition
- Product/regional performance ranking
- Year-over-year comparisons

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- 4GB+ RAM recommended
- Windows OS (Linux/Mac compatible with minor adjustments)

### **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AUREX-AI-Business-Intelligence.git
cd AUREX-AI-Business-Intelligence
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

5. **Start AUREX:**
```bash
# Windows
START_AUREX.bat

# Linux/Mac
chmod +x start_aurex.sh
./start_aurex.sh
```

6. **Access the application:**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔑 Configuration

### **Environment Variables (.env)**

```env
# LLM Configuration
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b

# LLM Parameters
LLM_MAX_TOKENS=1000
AGENT_TIMEOUT_SECONDS=90

# RAG Configuration
TOP_K=3
SIMILARITY_THRESHOLD=0.8

# Server Configuration
API_HOST=127.0.0.1
API_PORT=8000
FRONTEND_PORT=8501
```

### **Get Groq API Key**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for free account
3. Generate API key
4. Add to `.env` file

---

## 📖 Usage Guide

### **1. Upload Documents**
- Navigate to "Upload" page
- Drag & drop or select files (CSV, PDF, DOCX, TXT)
- System automatically processes and embeds documents
- Documents appear in the database within seconds

### **2. Ask Questions (AI Assistant)**
- Go to "AI Business Analyst" page
- Type natural language questions:
  - "What is the total revenue for 2024?"
  - "Which products are performing best?"
  - "Show me profit margins by region"
- Receive AI-generated answers with source citations
- Response time: ~2 seconds

### **3. Generate Reports**
- Open "Reports" page
- Select report type:
  - **Executive**: High-level summary for stakeholders
  - **Detailed**: Comprehensive analysis with all metrics
  - **Summary**: Quick overview of key findings
- Enable "Demo Mode" for instant results
- Download reports in HTML, Markdown, or JSON format

### **4. View Dashboard**
- Check "Dashboard" for real-time metrics
- View uploaded documents and processing status
- Monitor system health

---

## 🎯 Use Cases

### **Business Analytics**
- Revenue and profit analysis
- Product portfolio performance evaluation
- Regional market analysis
- Customer behavior insights

### **Executive Reporting**
- Automated quarterly/annual reports
- Board meeting presentations
- Stakeholder communications
- KPI tracking and monitoring

### **Data Exploration**
- Natural language data queries
- Ad-hoc analysis without SQL
- Quick insights from large datasets
- Multi-document information synthesis

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Python 3.11+ |
| **Frontend** | Streamlit |
| **LLM** | Groq API (openai/gpt-oss-120b) |
| **Vector DB** | ChromaDB |
| **Embeddings** | Sentence Transformers |
| **Data Processing** | Pandas, NumPy |
| **PDF Processing** | PyMuPDF |
| **API Client** | HTTPX |
| **Logging** | Python logging |

---

## 📊 Performance Metrics

- **Query Response Time**: 1.9 seconds average
- **Document Processing**: Real-time embedding
- **Vector Search**: Sub-100ms similarity search
- **Concurrent Users**: Supports multiple simultaneous queries
- **Scalability**: Handles 10,000+ document chunks

---

## 🗂️ Project Structure

```
AUREX/
├── app/
│   ├── api/              # FastAPI routes and endpoints
│   ├── rag/              # RAG pipeline and query engine
│   ├── analytics/        # Analytics and KPI extraction
│   ├── reports/          # Report generation
│   ├── data/             # Data processing and ingestion
│   ├── llm/              # LLM client integrations
│   ├── visualization/    # Chart generation
│   └── core/             # Core utilities and config
├── frontend/
│   ├── pages/            # Streamlit pages
│   └── app.py           # Main Streamlit app
├── data/
│   ├── raw/              # Uploaded documents
│   ├── chroma_db/        # Vector database
│   └── reports/          # Generated reports
├── tests/                # Unit and integration tests
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── START_AUREX.bat       # Start script (Windows)
└── README.md             # This file
```

---

## 🔒 Security & Privacy

- ✅ All data processed locally (except LLM API calls)
- ✅ API keys stored in `.env` (not committed to Git)
- ✅ No data retention by Groq API
- ✅ Documents stored only on your system
- ✅ No external data sharing

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Known Issues & Limitations

- Large PDF files (>50MB) may take longer to process
- Scanned PDFs require OCR (not included)
- Best results with structured business documents
- Groq API rate limits may apply (check [groq.com](https://groq.com))

---

## 🛣️ Roadmap

- [ ] Multi-language support
- [ ] Advanced visualization (interactive charts)
- [ ] SQL database integration
- [ ] Real-time data streaming
- [ ] Mobile-responsive UI
- [ ] Export to PowerPoint/Excel
- [ ] Custom ML model fine-tuning
- [ ] Multi-user authentication

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AUREX-AI-Business-Intelligence/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AUREX-AI-Business-Intelligence/discussions)

---

## 🌟 Acknowledgments

- [Groq](https://groq.com) for lightning-fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Streamlit](https://streamlit.io/) for rapid UI development
- [FastAPI](https://fastapi.tiangolo.com/) for high-performance backend

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### AI Assistant
![AI Assistant](docs/screenshots/ai-assistant.png)

### Reports
![Reports](docs/screenshots/reports.png)

---

**Made with ❤️ using AI and Python**

⭐ **Star this repo if you find it useful!**
