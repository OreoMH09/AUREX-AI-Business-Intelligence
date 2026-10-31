# AUREX Error Explanation

## 🔴 The Error You Saw

```
Unable to connect to backend API. Please ensure the FastAPI server is running on port 8000

Error: WinError [10061] No connection could be made because the target machine actively refused it
```

---

## 🎯 Why This Error Happened

### Simple Explanation:
**The frontend (Streamlit on port 8501) cannot talk to the backend (FastAPI on port 8000).**

Think of it like this:
- **Frontend** = The pretty website you see (Streamlit)
- **Backend** = The brain doing all the work (FastAPI)
- **Error** = The website can't find the brain!

### Technical Explanation:

AUREX has 2 parts that must run together:

1. **Backend Server** (FastAPI)
   - Runs on port 8000
   - Handles PDF processing, RAG queries, analytics
   - Provides API endpoints for frontend

2. **Frontend Server** (Streamlit)
   - Runs on port 8501
   - Shows the UI to users
   - Calls backend API to do work

**What went wrong:**
- The backend started but got stuck or crashed silently
- Port 8000 is occupied by a zombie process
- Frontend started successfully but can't reach backend
- Result: "Connection refused" error

---

## 🔍 What I Found

When I investigated:

1. ✅ **Frontend IS running** (port 8501, you can see the page)
2. ❌ **Backend NOT responding** (port 8000, but stuck/crashed)
3. ⚠️ **Port 8000 occupied** by process 12860 (zombie Python process)

---

## ✅ Solution: Restart Everything Clean

I created `RESTART_AUREX.bat` which will:

### Step 1: Kill Everything
- Stop all Python processes
- Free ports 8000 and 8501
- Clean slate!

### Step 2: Start Backend First
- Starts FastAPI server
- Waits 10 seconds for it to initialize
- Gives time to load models, connect to ChromaDB

### Step 3: Start Frontend
- Starts Streamlit UI
- Now it can connect to the ready backend!

---

## 🚀 How to Fix Right Now

### Option 1: Use Restart Script (Recommended)

**Double-click:**
```
RESTART_AUREX.bat
```

**OR run in terminal:**
```powershell
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
RESTART_AUREX.bat
```

**Wait 15-20 seconds**, then open: http://localhost:8501

---

### Option 2: Manual Restart

If the script doesn't work:

**Step 1: Kill all Python processes**
```powershell
taskkill /F /IM python.exe /T
```

**Step 2: Wait 5 seconds**
```powershell
timeout /t 5
```

**Step 3: Start backend first**
```powershell
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
venv\Scripts\activate
set PYTHONPATH=%CD%
python app/main.py
```

**Step 4: In a NEW terminal, start frontend**
```powershell
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
venv\Scripts\activate
set PYTHONPATH=%CD%
streamlit run frontend/streamlit_app.py
```

---

## 🛠️ Common Causes of This Error

### 1. Backend Crashed During Startup
**Why:** Missing dependencies, ChromaDB issues, Ollama not running
**Fix:** Check backend window for error messages

### 2. Port Already in Use
**Why:** Previous AUREX instance still running
**Fix:** Use RESTART_AUREX.bat to kill everything first

### 3. ChromaDB Not Running
**Why:** ChromaDB service not started or crashed
**Fix:** Ensure ChromaDB is running (if using external instance)

### 4. Ollama Not Running
**Why:** Backend tries to connect to Ollama but it's not started
**Fix:** Start Ollama before starting AUREX

### 5. Wrong Virtual Environment
**Why:** Backend started without activating venv
**Fix:** Always activate venv first: `venv\Scripts\activate`

---

## 🔎 How to Prevent This Error

### Before Starting AUREX:

1. **Make sure Ollama is running:**
   ```powershell
   ollama serve
   ```

2. **Use the startup script** (it handles order correctly):
   ```powershell
   START_AUREX.bat
   ```

3. **Wait patiently** - Backend takes 10-15 seconds to start

4. **Check the backend window** - Look for errors

5. **Don't close the terminal windows** - They need to stay open

---

## 📊 Port Reference

| Service | Port | Purpose | Must Be Running |
|---------|------|---------|-----------------|
| **Backend (FastAPI)** | 8000 | API, processing, RAG | ✅ Yes |
| **Frontend (Streamlit)** | 8501 | User interface | ✅ Yes |
| **ChromaDB** | 8001 | Vector database | ⚠️ If external |
| **Ollama** | 11434 | LLM inference | ✅ Yes |

---

## ✅ Quick Checklist

Before reporting an error, check:

- [ ] Is Ollama running? (`ollama list` should work)
- [ ] Did you use `START_AUREX.bat` or `RESTART_AUREX.bat`?
- [ ] Did you wait 15-20 seconds after starting?
- [ ] Can you see TWO windows (Backend + Frontend)?
- [ ] Is the Backend window showing errors?
- [ ] Did you activate the virtual environment?

---

## 🆘 If Error Persists

If after running `RESTART_AUREX.bat` you still see the error:

1. **Look at the Backend window** (the black cmd window)
2. **Take a screenshot** of any error messages
3. **Check if these services are running:**
   ```powershell
   # Check Ollama
   ollama list
   
   # Check ports
   netstat -ano | findstr "8000 8501 11434"
   ```

4. **Common fixes:**
   - Restart Ollama: Close and reopen Ollama
   - Reboot computer: Sometimes ports get stuck
   - Check antivirus: Might be blocking ports
   - Check firewall: Allow Python and ports 8000, 8501

---

## 💡 Summary

**Error**: Frontend can't connect to Backend
**Cause**: Backend stuck/crashed or port blocked
**Fix**: Run `RESTART_AUREX.bat`
**Prevention**: Always use startup scripts, ensure Ollama running

**Your AUREX application is fine - this is just a startup order issue!** 🎯
