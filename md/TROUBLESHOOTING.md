# 🔧 AUREX TROUBLESHOOTING GUIDE

## ⚠️ "Unable to connect to backend API"

### **Symptom:**
Frontend shows: "Unable to connect to backend API. Please ensure the FastAPI server is running on port 8000"

### **Solution:**

#### Quick Fix:
1. **Refresh the browser** (Press F5)
2. Wait 5-10 seconds
3. Refresh again

The backend takes a few seconds to start up.

---

#### If that doesn't work:

**Method 1: Check if backend is running**
```bash
# Open browser and go to:
http://localhost:8000/api/docs

# If you see API documentation, backend is working!
```

**Method 2: Restart backend manually**
1. Close the "AUREX Backend" window
2. Double-click `start_backend.bat`
3. Wait for "Application startup complete"
4. Go back to frontend and refresh

---

## 🐛 Common Issues & Fixes

### Issue 1: "Port already in use"

**Solution:**
Edit `.env` file:
```
API_PORT=8001
STREAMLIT_PORT=8502
```

Then restart.

---

### Issue 2: "No module named 'app'"

**Solution:**
Use the startup scripts (`start_backend.bat`) instead of running `python app/main.py` directly.

The scripts automatically set PYTHONPATH.

---

### Issue 3: Backend window closes immediately

**Solution:**
1. Open `start_backend.bat` in a terminal to see the error
2. Or run manually:
```bash
venv\Scripts\activate
set PYTHONPATH=%CD%
python app/main.py
```

Common causes:
- Virtual environment not created: `python -m venv venv`
- Dependencies not installed: `pip install -r requirements.txt`

---

### Issue 4: Frontend opens but shows blank page

**Solution:**
1. Check browser console (F12)
2. Make sure backend started successfully
3. Try a different browser (Chrome/Edge/Firefox)

---

### Issue 5: "fitz API is deprecated" warning

**Don't worry!** This is just a warning, not an error. Everything still works fine.

---

## 🔍 How to Check If Things Are Running

### Check Backend:
```bash
# Visit this URL in browser:
http://localhost:8000/api/health

# Should show:
{
  "status": "healthy",
  "version": "1.0.0",
  ...
}
```

### Check Frontend:
```bash
# Visit this URL in browser:
http://localhost:8501

# Should show the AUREX home page
```

---

## 🚀 Recommended Startup Order

1. **Start Backend First**
   ```bash
   start_backend.bat
   ```
   Wait for: "Application startup complete"

2. **Then Start Frontend**
   ```bash
   start_frontend.bat
   ```
   Wait for browser to open

3. **If using ONE-CLICK launcher**
   ```bash
   START_AUREX.bat
   ```
   Wait 10 seconds after windows open, then refresh browser

---

## 🔄 How to Restart Properly

1. Close both windows (Backend + Frontend)
2. Wait 5 seconds
3. Start again with `START_AUREX.bat`

---

## 📞 Still Having Issues?

### Check these files for details:
- `HOW_TO_RUN.md` - Complete running instructions
- `ISSUE_FIXED.md` - Common module import issues
- `SETUP_COMPLETE.md` - Full setup guide

### Verify your setup:
```bash
venv\Scripts\activate
python scripts/verify_stage5.py
```

---

## ✅ Quick Checklist

Before asking for help, verify:
- [ ] Virtual environment exists (`venv/` folder)
- [ ] Dependencies installed (`pip list` shows many packages)
- [ ] `.env` file exists
- [ ] Backend window stays open (doesn't close immediately)
- [ ] You waited at least 10 seconds after startup
- [ ] Tried refreshing the browser (F5)

---

## 💡 Pro Tips

1. **Always use the startup scripts** instead of manual commands
2. **Wait 10 seconds** after starting before expecting everything to work
3. **Backend must start first** - frontend connects to it
4. **Check backend URL** (http://localhost:8000/api/docs) to confirm it's running

---

**Most issues are solved by: Close everything → Wait 5 seconds → Run START_AUREX.bat → Wait 10 seconds → Refresh browser**
