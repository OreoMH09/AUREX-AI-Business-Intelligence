# AUREX - Quick Start Guide

## 🚀 Get Started in 5 Steps

### Step 1: Install Dependencies
```bash
# This will take 5-10 minutes
pip install -r requirements.txt
```

### Step 2: Install Ollama
```bash
# Windows: Download from https://ollama.ai and install
# Then pull the model:
ollama pull llama3.1:8b
```

### Step 3: Start Ollama (if not running as service)
```bash
ollama serve
```

### Step 4: Start the Backend (New Terminal)
```bash
python app/main.py
```
Visit: http://localhost:8000/api/docs

### Step 5: Start the Frontend (New Terminal)
```bash
streamlit run frontend/streamlit_app.py
```
Visit: http://localhost:8501

---

## ✅ Verify Installation

### Check Backend Health
```bash
curl http://localhost:8000/api/health
```

### Run Tests
```bash
pytest
```

---

## 📁 What's Implemented (Stages 1-4)

✅ **Backend API** - FastAPI with health endpoints  
✅ **Frontend UI** - Streamlit multi-page app  
✅ **Configuration** - Environment-based settings  
✅ **Logging** - Structured logs (console + file)  
✅ **Testing** - pytest framework  
✅ **Docker** - Containerization ready  
✅ **Documentation** - Complete guides  

---

## 🚧 What's Coming Next (Stage 5+)

Stage 5: PDF document ingestion and parsing  
Stage 6: Excel and CSV processing  
Stage 7: Metadata extraction and profiling  
Stage 8: Vector embeddings and ChromaDB  
Stage 9: RAG semantic retrieval  
Stage 10: LLM-powered question answering  
...and 10 more stages!

---

## 📚 Key Documents

- `README.md` - Complete project documentation
- `BUILD_STATUS.md` - Detailed build progress
- `PROJECT_TRACKER.md` - Stage-by-stage checklist
- `AUREX_KIRO_Master_Build_Prompt.md` - Original specification

---

## 🆘 Troubleshooting

**Port Already in Use?**
```bash
# Change ports in .env file:
API_PORT=8001
STREAMLIT_PORT=8502
```

**Ollama Not Working?**
```bash
# Check if Ollama is running:
ollama list

# Restart Ollama service
```

**Import Errors?**
```bash
# Ensure you're in the virtual environment:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

---

**Happy Building! 🎉**
