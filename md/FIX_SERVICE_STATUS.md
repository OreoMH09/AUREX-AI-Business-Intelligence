# Fix for Services Showing "Unavailable"

## Issue Found

Your services were showing:
- ✅ Vector DB: **healthy** (1/3)
- ❌ LLM: **unavailable**
- ❌ Embeddings: **unavailable**

## Root Causes

### 1. **Embeddings Health Check - Wrong Import Path**
**Problem:** Health check was trying to import:
```python
from app.embeddings.sentence_transformer import get_embeddings
```

**But:** The actual location is:
```python
from app.vector_store.embeddings import get_embedding_service
```

**Error:** `ModuleNotFoundError` - the `app.embeddings` module doesn't exist!

### 2. **LLM Health Check - Wrong Attribute**
**Problem:** Health check was checking:
```python
if ollama_client.client:  # ❌ This attribute doesn't exist
```

**But:** Should use the actual health check method:
```python
if ollama_client.check_health():  # ✅ This method exists
```

**Error:** `AttributeError` - OllamaClient has no `.client` attribute

## Fixes Applied

### Fix 1: Embeddings Import Path ✅
**File:** `app/api/routes/health.py`

**Changed from:**
```python
from app.embeddings.sentence_transformer import get_embeddings
embeddings_model = get_embeddings()
if embeddings_model.model:
```

**Changed to:**
```python
from app.vector_store.embeddings import get_embedding_service
embeddings_service = get_embedding_service()
if embeddings_service.model:
```

### Fix 2: Ollama Health Check Method ✅
**File:** `app/api/routes/health.py`

**Changed from:**
```python
if ollama_client.client:
```

**Changed to:**
```python
if ollama_client.check_health():
```

This uses the actual `check_health()` method that:
- Connects to Ollama server at `http://localhost:11434`
- Calls `/api/tags` endpoint
- Returns `True` if server responds with 200 status

## How to Apply

### Step 1: Stop AUREX
```powershell
taskkill /F /IM python.exe /T
```

### Step 2: Restart AUREX
```powershell
RESTART_AUREX.bat
```

### Step 3: Verify Services (http://localhost:8501)

You should now see:
- ✅ Vector DB: **healthy**
- ✅ LLM: **healthy**
- ✅ Embeddings: **healthy**
- **Services Status: 3/3** 🎉

## What Each Service Does

### 1. Vector DB (ChromaDB)
- Stores document embeddings
- Enables semantic search
- **Status:** Already working ✅
- **Location:** `data/chroma_db`

### 2. LLM (Ollama)
- Generates natural language responses
- **Model:** llama3.1:8b
- **Port:** 11434
- **Check:** `ollama list` should show your model

### 3. Embeddings (SentenceTransformer)
- Converts text to vector embeddings
- **Model:** all-MiniLM-L6-v2
- **Dimension:** 384
- **Type:** Local (no internet needed)

## If LLM Still Shows Unavailable

### Check if Ollama is running:
```powershell
ollama list
```

Should output:
```
NAME              ID              SIZE      MODIFIED
llama3.1:8b       abc123def...    4.7 GB    X days ago
```

### If Ollama not running:
```powershell
ollama serve
```

Or check if it's in Windows Services and set to start automatically.

## If Embeddings Still Shows Unavailable

### Check if model can be loaded:
```powershell
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('✅ Model loaded')"
```

Should print: `✅ Model loaded`

### If model fails to load:
First time loading downloads the model (about 80MB):
```
Downloading model files...
100%|████████████████████████████████| 80M/80M
✅ Model loaded
```

## Expected Behavior After Restart

### Backend Console Should Show:
```
INFO: Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
INFO: Embedding model loaded successfully (dimension: 384)
INFO: OllamaClient initialized: http://localhost:11434, model: llama3.1:8b
INFO: Discovering existing documents in data/raw
INFO: Discovered 19 existing documents
INFO: DocumentService initialized with 19 documents
INFO: Application startup complete
```

### Home Page Should Show:
```
System Status
API Status: HEALTHY
Version: 1.0.0
Environment: development
Services: 3/3

Services Status:
Vector Db        Llm           Embeddings
✅ healthy      ✅ healthy    ✅ healthy
```

## Troubleshooting

### If Vector DB becomes unavailable after fixes:
```powershell
# Check if ChromaDB folder exists
ls data/chroma_db

# If it doesn't exist, create it
mkdir data/chroma_db
```

### If all services show unavailable:
Backend might have crashed on startup. Check the backend console window for error messages.

Common errors:
- `ModuleNotFoundError`: Missing dependency, run `pip install -r requirements.txt`
- `ConnectionRefusedError`: Ollama not running, start with `ollama serve`
- `RuntimeError`: Model download failed, check internet connection

## Summary

✅ **Fixed embeddings import** - Correct path: `app.vector_store.embeddings`  
✅ **Fixed LLM health check** - Using `check_health()` method  
✅ **All 3 services should now show healthy**  
✅ **Services Status: 3/3** 🎉

**Just restart AUREX and all services should be green!**
