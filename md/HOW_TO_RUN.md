# 🚀 HOW TO RUN AUREX

## ⚡ SUPER EASY - ONE-CLICK START

**Just double-click:**
```
START_AUREX.bat
```

This opens **TWO windows**:
1. Backend Server (FastAPI)
2. Frontend UI (Streamlit)

Your browser will open automatically to http://localhost:8501

**That's it!** 🎉

---

## ✅ Quick Start (Individual Scripts)

### Method 1: Using Startup Scripts (Recommended)

**Start Backend:**
```bash
# Double-click or run:
start_backend.bat
```

**Start Frontend** (in a new terminal):
```bash
# Double-click or run:
start_frontend.bat
```

That's it! The scripts handle everything automatically.

---

## 🔧 Manual Start (Alternative)

### Step 1: Activate Virtual Environment
```bash
venv\Scripts\activate
```

### Step 2: Set PYTHONPATH and Start Backend
```bash
$env:PYTHONPATH = "$PWD"
python app/main.py
```

### Step 3: Start Frontend (New Terminal)
```bash
venv\Scripts\activate
$env:PYTHONPATH = "$PWD"
streamlit run frontend/streamlit_app.py
```

---

## 🌐 Access URLs

Once started, open your browser:

- **Frontend UI:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

---

## ⚠️ Troubleshooting

### Error: "No module named 'app'"

**Solution:** Set PYTHONPATH before running:
```bash
$env:PYTHONPATH = "$PWD"
```

Or use the provided startup scripts (they do this automatically).

### Error: "venv not found"

**Solution:** Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Port Already in Use

**Solution:** Change ports in `.env`:
```
API_PORT=8001
STREAMLIT_PORT=8502
```

---

## 📋 What to Do After Starting

1. **Backend starts** - Wait for "Application startup complete"
2. **Frontend starts** - Browser opens automatically
3. **Go to Upload page** - Upload a PDF
4. **Try the sample PDF** - Located at `data/sample/sample_business_report_2025.pdf`

---

## 🛑 How to Stop

Press `Ctrl+C` in each terminal window.

---

## 📝 Quick Commands

| Action | Command |
|--------|---------|
| Start Backend | `start_backend.bat` |
| Start Frontend | `start_frontend.bat` |
| Run Tests | `pytest` |
| Create Sample PDF | `python scripts/create_sample_pdf.py` |
| Verify Setup | `python scripts/verify_stage5.py` |

---

## ✨ Tips

- **Always activate venv first** before manual commands
- **Use startup scripts** for hassle-free launching
- **Open 2 terminals** - one for backend, one for frontend
- **Backend must start first** before frontend

---

**Need help? Check `SETUP_COMPLETE.md` or `QUICKSTART.md`**
