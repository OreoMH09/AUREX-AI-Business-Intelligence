# How to Start AUREX - Complete Guide

## 🚀 Quick Start (Recommended)

### **Every Time You Want to Use AUREX:**

**Just double-click this file:**
```
START_AUREX.bat
```

**Then:**
1. Wait 20 seconds
2. Open browser: http://localhost:8501
3. Done! ✅

---

## 📋 Detailed Step-by-Step Guide

### **Method 1: Using START_AUREX.bat** (Easiest - Use This!)

#### Step 1: Make Sure Nothing is Running

Before starting, check if AUREX is already running:
- Look for windows titled "AUREX Backend" or "AUREX Frontend"
- If found, close them first

#### Step 2: Start AUREX

**Option A: Double-click**
- Find `START_AUREX.bat` in your AUREX folder
- Double-click it

**Option B: Run in terminal**
```powershell
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
START_AUREX.bat
```

#### Step 3: Watch for Two Windows

You should see **2 new windows** open:

1. **"AUREX Backend - python app/main.py"**
   - This is a black command window
   - Shows backend server logs
   - **DON'T CLOSE THIS!**

2. **"AUREX Frontend - streamlit run frontend/streamlit_app.py"**
   - Another command window
   - Shows frontend logs
   - **DON'T CLOSE THIS!**

#### Step 4: Wait for Backend to Start

In the Backend window, look for this line:
```
INFO:     Started server process [19688]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**This means backend is ready!** ✅

#### Step 5: Wait for Frontend to Start

In the Frontend window, look for:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

**This means frontend is ready!** ✅

#### Step 6: Open Browser

Open your browser and go to:
```
http://localhost:8501
```

Wait 5-10 seconds for the page to load.

**AUREX is now running!** 🎉

---

### **Method 2: Using RESTART_AUREX.bat** (If Problems Occur)

If `START_AUREX.bat` gives errors or AUREX is stuck:

#### Use RESTART_AUREX.bat Instead:

**This script will:**
1. Kill all running Python processes
2. Clear ports 8000 and 8501
3. Start backend fresh
4. Start frontend fresh

**How to use:**
```powershell
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
RESTART_AUREX.bat
```

Or just double-click `RESTART_AUREX.bat`

---

### **Method 3: Manual Start** (Advanced - If Scripts Don't Work)

#### Terminal 1 - Start Backend:

```powershell
# Navigate to AUREX folder
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"

# Activate virtual environment
venv\Scripts\activate

# Set Python path
set PYTHONPATH=%CD%

# Start backend
python app/main.py
```

**Keep this terminal open!**

#### Terminal 2 - Start Frontend:

Open a **NEW terminal** and run:

```powershell
# Navigate to AUREX folder
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"

# Activate virtual environment
venv\Scripts\activate

# Set Python path
set PYTHONPATH=%CD%

# Start frontend
streamlit run frontend/streamlit_app.py
```

**Keep this terminal open too!**

#### Open Browser:
```
http://localhost:8501
```

---

## 🔄 How to Restart AUREX

### **If AUREX is Already Running:**

#### Option 1: Close and Restart
1. Close both terminal windows (Backend + Frontend)
2. Wait 5 seconds
3. Run `START_AUREX.bat` again

#### Option 2: Use RESTART Script
```powershell
RESTART_AUREX.bat
```

#### Option 3: Kill Processes Manually
```powershell
# Kill all Python processes
taskkill /F /IM python.exe /T

# Wait 3 seconds
timeout /t 3

# Start again
START_AUREX.bat
```

---

## ⚠️ Common Problems & Solutions

### Problem 1: "Port 8000 is already in use"

**Cause**: Backend from previous run still running

**Solution**:
```powershell
# Kill Python processes
taskkill /F /IM python.exe /T

# Wait and restart
timeout /t 3
START_AUREX.bat
```

### Problem 2: "Unable to connect to backend API"

**Cause**: Backend not started or crashed

**Solution**:
1. Check Backend window for errors
2. Look for line: "Started server process"
3. If not found, restart using `RESTART_AUREX.bat`

### Problem 3: Browser Shows "Site Can't Be Reached"

**Cause**: Frontend not started

**Solution**:
1. Check Frontend window
2. Look for: "Local URL: http://localhost:8501"
3. Wait 10 more seconds
4. Try refreshing browser

### Problem 4: CSV File Upload Fails

**Possible Issues**:
1. **CSV encoding problem** - Try saving CSV as UTF-8
2. **Large file** - Keep CSV under 10MB
3. **Special characters** - Remove special chars from column names
4. **Empty CSV** - Make sure CSV has data

**Quick Test**:
1. Try uploading the sample file: `data/sample/sample_business_report_2025.pdf`
2. If PDF works but CSV doesn't, the CSV file might have issues

**CSV Upload Tips**:
- Save CSV with UTF-8 encoding
- Use simple column names (no spaces/special chars)
- Keep file size reasonable (<5MB recommended)
- Make sure first row has column headers

---

## 📊 Checking if AUREX is Running

### **Method 1: Check Processes**

```powershell
# Check if Python is running
tasklist | findstr python
```

Should show multiple python.exe processes

### **Method 2: Check Ports**

```powershell
# Check if ports are in use
netstat -ano | findstr "8000 8501"
```

Should show:
- Port 8000 (Backend)
- Port 8501 (Frontend)

### **Method 3: Use CHECK_STATUS.bat**

```powershell
CHECK_STATUS.bat
```

This shows if backend and frontend are running.

### **Method 4: Open Browser**

Try opening: http://localhost:8501

If AUREX loads, it's running! ✅

---

## 🛑 How to Stop AUREX

### **Method 1: Close Windows**
Simply close both terminal windows (Backend + Frontend)

### **Method 2: Kill Processes**
```powershell
taskkill /F /IM python.exe /T
```

### **Method 3: Press Ctrl+C**
In each terminal window:
1. Click inside the window
2. Press `Ctrl + C`
3. Wait for it to stop

---

## 🎯 Best Practices

### **Starting AUREX:**
1. ✅ Always use `START_AUREX.bat`
2. ✅ Wait 20-30 seconds before opening browser
3. ✅ Check Backend window for "Started server process"
4. ✅ Keep both terminal windows open
5. ✅ Bookmark http://localhost:8501 in your browser

### **Stopping AUREX:**
1. ✅ Close browser first
2. ✅ Then close terminal windows
3. ✅ OR use: `taskkill /F /IM python.exe /T`

### **Restarting AUREX:**
1. ✅ Use `RESTART_AUREX.bat` (handles everything)
2. ✅ Or close windows and use `START_AUREX.bat`

---

## 🆘 Emergency Recovery

**If nothing works:**

### **Step 1: Clean Slate**
```powershell
# Kill everything
taskkill /F /IM python.exe /T
taskkill /F /IM python3.exe /T
taskkill /F /IM pythonw.exe /T

# Wait
timeout /t 5
```

### **Step 2: Restart Computer**
If really stuck, just restart your computer!

### **Step 3: Fresh Start**
After restart:
```powershell
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
START_AUREX.bat
```

---

## 📝 Quick Reference Card

| Action | Command |
|--------|---------|
| **Start AUREX** | `START_AUREX.bat` |
| **Restart AUREX** | `RESTART_AUREX.bat` |
| **Check Status** | `CHECK_STATUS.bat` |
| **Stop AUREX** | Close terminal windows |
| **Kill Processes** | `taskkill /F /IM python.exe /T` |
| **Open Frontend** | http://localhost:8501 |
| **Open API Docs** | http://localhost:8000/api/docs |

---

## 💡 Pro Tips

1. **Create Desktop Shortcut**:
   - Right-click `START_AUREX.bat`
   - Select "Create shortcut"
   - Move shortcut to Desktop
   - Now you can start AUREX from Desktop!

2. **Bookmark URLs**:
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/api/docs

3. **Keep Windows Visible**:
   - Arrange Backend and Frontend windows side-by-side
   - Easy to see if any errors occur

4. **Wait Patiently**:
   - First start takes 20-30 seconds
   - Dashboard first load takes 30-60 seconds
   - Be patient, don't refresh immediately!

---

## ✅ Success Checklist

Before using AUREX, verify:

- [ ] Two terminal windows open (Backend + Frontend)
- [ ] Backend window shows "Started server process"
- [ ] Frontend window shows "Local URL: http://localhost:8501"
- [ ] Browser opens http://localhost:8501
- [ ] AUREX page loads (may take 30 seconds)
- [ ] No red error messages

**All checked?** You're ready to use AUREX! 🎉

---

## 📞 Need Help?

If you're still having issues:

1. **Check Backend window** - Look for error messages
2. **Check Frontend window** - Look for error messages
3. **Run CHECK_STATUS.bat** - See what's running
4. **Try RESTART_AUREX.bat** - Fresh clean start
5. **Restart computer** - Last resort but works!

---

**Remember**: Always use `START_AUREX.bat` - it handles everything for you! 🚀
