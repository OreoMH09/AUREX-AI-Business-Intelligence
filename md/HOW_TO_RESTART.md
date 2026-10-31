# How to Restart AUREX After Fixes

## Quick Restart (Recommended)

### Option 1: Use RESTART_AUREX.bat
```powershell
RESTART_AUREX.bat
```
This will:
1. Kill all running Python processes
2. Wait 2 seconds
3. Start backend and frontend fresh

### Option 2: Use START_AUREX.bat
First stop everything:
```powershell
taskkill /F /IM python.exe /T
```

Then start:
```powershell
START_AUREX.bat
```

## What to Expect After Restart

### In Backend Window (Port 8000)
You should see these logs:
```
INFO: Discovering existing documents in data/raw
DEBUG: Discovered document: 95c864b3-29f8-43da-b50a-72ce8b64fc0e - Orders_2024.csv
DEBUG: Discovered document: cef8247a-1eac-422c-b62a-2a4a3f193b1a - Orders.xlsx
... (more documents)
INFO: Discovered 19 existing documents
INFO: DocumentService initialized with 19 documents
INFO: Application startup complete
INFO: Uvicorn running on http://127.0.0.1:8000
```

### In Frontend Browser (http://localhost:8501)

**Home Page:**
- Services Status: **3/3** ✅
- Vector DB: **healthy** ✅
- LLM: **healthy** ✅
- Embeddings: **healthy** ✅

**Upload Page:**
- Total documents: **19** ✅
- List showing all your files ✅
- Duplicate warnings for files uploaded twice ✅
- Delete buttons working ✅

## Verification Steps

1. **Open Backend Window** - Check for "Discovered 19 existing documents"
2. **Open http://localhost:8501** - Home page should show 3/3 services healthy
3. **Click "📤 Upload" page** - Should see all 19 documents listed
4. **Check for duplicates** - Files marked with "⚠️ DUPLICATE" warning

## If Something Goes Wrong

### Backend won't start:
```powershell
# Check if port is already in use
netstat -ano | findstr "8000"

# Kill the process using port 8000
taskkill /F /PID <PID_NUMBER>

# Try starting again
START_AUREX.bat
```

### Documents still not showing:
1. Check files exist:
```powershell
ls data/raw
```
2. Check backend logs for "Discovered X documents"
3. Restart backend again

### Services showing unavailable:
1. Check Ollama is running:
```powershell
ollama list
```
2. Check ChromaDB folder exists:
```powershell
ls data/chroma
```

## Normal Startup Flow

1. Backend starts on port 8000
2. Backend discovers 19 documents from data/raw
3. Backend initializes ChromaDB, Ollama, Embeddings
4. Frontend starts on port 8501
5. Frontend connects to backend API
6. Services show healthy
7. Documents list shows all 19 files

**That's it! Just restart and everything should work! 🚀**
