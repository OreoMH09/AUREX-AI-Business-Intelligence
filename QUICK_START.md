# ⚡ AUREX Quick Start Guide

## 🚀 For New Users

### **1. Install Prerequisites**
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/downloads))

### **2. Get Groq API Key (Free)**
1. Visit https://console.groq.com
2. Sign up (free account)
3. Click "Create API Key"
4. Copy the key (starts with `gsk_...`)

### **3. Clone & Setup**
```bash
# Clone repository
git clone https://github.com/yourusername/AUREX-AI-Business-Intelligence.git
cd AUREX-AI-Business-Intelligence

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure
copy .env.example .env
notepad .env  # Add your Groq API key
```

### **4. Start AUREX**
```bash
# Windows - Easy way
START_AUREX.bat

# Or manually
# Terminal 1: Backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend  
streamlit run frontend/app.py --server.port 8501
```

### **5. Open Browser**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

---

## 📖 First Time Usage

### **Upload Documents**
1. Click "Upload" in sidebar
2. Drag files (CSV, PDF, Excel, TXT)
3. Wait for "Processing complete"

### **Ask Questions**
1. Go to "AI Business Analyst"
2. Type: "What is the total revenue?"
3. Get answer in ~2 seconds

### **Generate Reports**
1. Open "Reports"
2. Keep "Demo Mode" checked for instant results
3. Click "Generate Report"
4. Preview and download

---

## 🔧 Configuration (.env file)

**Minimum required:**
```env
GROQ_API_KEY=gsk_your_key_here
```

**Full configuration:**
```env
# LLM
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=openai/gpt-oss-120b
LLM_MAX_TOKENS=1000

# RAG
TOP_K=3
SIMILARITY_THRESHOLD=0.8

# Server
API_HOST=127.0.0.1
API_PORT=8000
```

---

## 🎯 Example Queries

**Revenue Questions:**
- "What is the total revenue?"
- "Show revenue by region"
- "What was Q4 revenue?"

**Product Analysis:**
- "Which products are top performers?"
- "Compare Product A vs Product B"
- "What are the sales trends?"

**Insights:**
- "What are the key business insights?"
- "Show profit margin analysis"
- "What recommendations do you have?"

---

## 🛠️ Troubleshooting

### **Backend won't start**
```bash
# Check port 8000 is free
netstat -ano | findstr :8000

# Kill process if needed (Windows)
taskkill /F /PID <PID>
```

### **"Module not found" error**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Groq API error**
- Verify API key in `.env`
- Check internet connection
- Visit https://console.groq.com to verify key is active

### **Streamlit port already in use**
```bash
# Use different port
streamlit run frontend/app.py --server.port 8502
```

---

## 📊 System Requirements

**Minimum:**
- Python 3.11+
- 4GB RAM
- 1GB disk space
- Internet connection (for Groq API)

**Recommended:**
- Python 3.11+
- 8GB+ RAM
- 5GB disk space (for documents)
- Stable internet

---

## 🔄 Restart/Stop

### **Restart**
```bash
RESTART_AUREX.bat  # Windows
```

### **Stop**
- Press `Ctrl+C` in both terminal windows
- Or close terminals

---

## 📝 File Formats Supported

✅ **CSV** - Comma-separated values  
✅ **PDF** - Business reports, documents  
✅ **Excel** - .xlsx, .xls files  
✅ **Text** - .txt files  
✅ **Word** - .docx files  

---

## 🆘 Need Help?

- **Documentation**: Check README.md
- **Issues**: https://github.com/yourusername/AUREX-AI-Business-Intelligence/issues
- **Discussions**: https://github.com/yourusername/AUREX-AI-Business-Intelligence/discussions

---

## ⭐ Next Steps

1. Upload your business documents
2. Try example queries
3. Generate your first report
4. Explore the dashboard
5. Customize for your needs

**Enjoy AUREX! 🎉**
