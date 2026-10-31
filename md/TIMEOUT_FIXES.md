# AUREX Timeout Issues - Complete Fix Guide

## 🔴 Problems You're Experiencing

### 1. AI Business Analyst Timeout
**Error**: "Request timed out. The query is taking too long."
**Current Timeout**: 60 seconds
**Why**: Complex RAG queries + Ollama LLM processing takes longer

### 2. Dashboard KPIs Timeout
**Error**: "Error fetching KPIs: timed out"
**Current Timeout**: 30 seconds
**Why**: Analyzing all documents, calculating statistics takes time

### 3. Dashboard Charts Timeout
**Error**: "Error fetching charts: timed out"
**Current Timeout**: 30 seconds
**Why**: Generating multiple charts from document data takes time

---

## 🎯 Root Causes Explained

### Why Timeouts Happen:

1. **Large Documents**
   - More text = More chunks to embed
   - More chunks = Slower vector search
   - Result: Query takes longer

2. **Slow Ollama Response**
   - LLM generating detailed answers
   - Default model (llama2) can be slow
   - CPU inference slower than GPU

3. **Dashboard Loading ALL Documents**
   - Backend processes every uploaded document
   - Calculates aggregate statistics
   - Generates chart data for all
   - No per-document filtering optimization

4. **No Backend Caching**
   - Same queries recalculated every time
   - Dashboard data regenerated on each load
   - Embeddings recalculated unnecessarily

---

## ✅ Solutions (Multiple Approaches)

### Solution 1: Increase Timeouts (Quick Fix)

**Files to modify:**

#### A. Dashboard Page (`frontend/pages/3_📊_Dashboard.py`)

**Lines 86 & 108 - Change from:**
```python
timeout=30.0  # Current
```

**To:**
```python
timeout=180.0  # 3 minutes
```

#### B. AI Business Analyst (`frontend/pages/2_🤖_AI_Business_Analyst.py`)

**Line 228 - Change from:**
```python
timeout=60.0  # 1 minute
```

**To:**
```python
timeout=180.0  # 3 minutes
```

#### C. Ollama Client (`app/llm/ollama_client.py`)

**Lines 131, 158, 203 - Change from:**
```python
timeout=120  # 2 minutes
```

**To:**
```python
timeout=300  # 5 minutes
```

---

### Solution 2: Add Retry Logic (Better Fix)

Add automatic retries when timeout occurs.

**Dashboard fixes** (`frontend/pages/3_📊_Dashboard.py`):

Replace the `fetch_kpis` function (around line 75):

```python
import time

# Function to fetch KPIs
@st.cache_data(ttl=300)
def fetch_kpis(document_id=None):
    """Fetch KPIs from backend with retry logic"""
    max_retries = 2
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            params = {}
            if document_id:
                params['document_id'] = document_id
            
            # Increased timeout + retry
            response = httpx.get(
                f"http://{settings.api_host}:{settings.api_port}/api/analytics/kpis",
                params=params,
                timeout=180.0  # 3 minutes
            )
            
            if response.status_code == 200:
                return response.json()
            elif attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return None
            
        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                st.warning(f"⏱️ Loading KPIs... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                st.error("⏱️ Timeout loading KPIs. Try filtering by a specific document to reduce load.")
                return None
        except Exception as e:
            st.error(f"Error fetching KPIs: {e}")
            return None
    return None

# Function to fetch charts
@st.cache_data(ttl=300)
def fetch_charts(document_id=None):
    """Fetch visualization charts from backend with retry logic"""
    max_retries = 2
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            params = {}
            if document_id:
                params['document_id'] = document_id
            
            # Increased timeout + retry
            response = httpx.get(
                f"http://{settings.api_host}:{settings.api_port}/api/visualization/kpi-charts",
                params=params,
                timeout=180.0  # 3 minutes
            )
            
            if response.status_code == 200:
                return response.json()
            elif attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return None
            
        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                st.warning(f"⏱️ Loading charts... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                st.error("⏱️ Timeout loading charts. Try filtering by a specific document to reduce load.")
                return None
        except Exception as e:
            st.error(f"Error fetching charts: {e}")
            return None
    return None
```

---

### Solution 3: Add Progress Indicators (Best UX)

Show users that processing is happening, not frozen.

**AI Business Analyst** (`frontend/pages/2_🤖_AI_Business_Analyst.py`):

Replace the query handling (around line 215):

```python
        try:
            # Show processing indicator
            with st.spinner("🤔 Analyzing your question and searching documents..."):
                # Create request
                request_data = {
                    "query": query,
                    "use_agent": use_agent
                }
                if document_filter:
                    request_data["document_filter"] = document_filter
                
                # Send query to backend with longer timeout
                response = httpx.post(
                    f"http://{settings.api_host}:{settings.api_port}/api/query",
                    json=request_data,
                    timeout=180.0  # Increased to 3 minutes
                )
            
            if response.status_code == 200:
                result = response.json()
                
                # Add assistant message
                assistant_message = {
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result.get("sources", []),
                    "metadata": {
                        "retrieved_chunks": result.get("retrieved_chunks", 0),
                        "processing_time_ms": result.get("processing_time_ms", 0)
                    }
                }
                st.session_state.messages.append(assistant_message)
                
                # Show success message
                st.success(f"✅ Answer generated in {result.get('processing_time_ms', 0)/1000:.1f}s")
                
                # Rerun to display the new message
                st.rerun()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except httpx.TimeoutException:
            st.error("⏱️ Request timed out after 3 minutes. This can happen with:")
            st.markdown("""
            - Very complex questions requiring deep analysis
            - Large document collections (try filtering by document)
            - Slow Ollama model response
            
            **Tips to avoid timeout:**
            - Ask simpler, more specific questions
            - Filter by a single document
            - Use a faster Ollama model (e.g., phi, tinyllama)
            """)
```

---

### Solution 4: Backend Optimization (Advanced)

**Add caching to backend** (`app/rag/query_engine.py`):

```python
from functools import lru_cache
import hashlib

class QueryEngine:
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
    
    def _cache_key(self, query: str, document_filter: str = None) -> str:
        """Generate cache key from query"""
        key_str = f"{query}:{document_filter}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    async def query(self, query: str, document_filter: str = None):
        # Check cache first
        cache_key = self._cache_key(query, document_filter)
        if cache_key in self.cache:
            logger.info(f"Cache hit for query: {query[:50]}...")
            return self.cache[cache_key]
        
        # Process query...
        result = await self._process_query(query, document_filter)
        
        # Cache result (keep last 100)
        if len(self.cache) > 100:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))
        self.cache[cache_key] = result
        
        return result
```

---

## 🚀 Quick Implementation Guide

### Step 1: Choose Your Approach

**For immediate fix**: Use Solution 1 (increase timeouts)
**For better UX**: Use Solution 2 + 3 (retry + progress)
**For best performance**: Combine all solutions

### Step 2: Apply Changes

**Option A: Manual editing**
1. Open each file mentioned
2. Find the line numbers
3. Replace the code as shown
4. Save files
5. Restart AUREX

**Option B: Let me do it**
Say "apply timeout fixes" and I'll modify all files for you!

### Step 3: Test

1. Start AUREX: `START_AUREX.bat`
2. Go to Dashboard - check if KPIs load (may take up to 3 min)
3. Go to AI Business Analyst - ask a complex question
4. Verify no timeouts occur

---

## 📊 Timeout Recommendations

| Component | Current | Recommended | Reason |
|-----------|---------|-------------|--------|
| **AI Query** | 60s | 180s (3 min) | Complex RAG + LLM |
| **Dashboard KPIs** | 30s | 180s (3 min) | Multi-document analysis |
| **Dashboard Charts** | 30s | 180s (3 min) | Chart generation |
| **Ollama Generate** | 120s | 300s (5 min) | LLM inference |
| **File Upload** | 30s | 60s (1 min) | Large PDFs |

---

## 💡 User Tips to Avoid Timeouts

### For AI Business Analyst:
1. **Ask specific questions** instead of broad ones
2. **Filter by single document** when possible
3. **Use simpler language** (easier for LLM to process)
4. **Break complex questions** into multiple simpler ones

### For Dashboard:
1. **Filter by document ID** instead of loading all
2. **Use the refresh button** sparingly
3. **Wait for initial load** before changing filters
4. **Clear browser cache** if stuck loading

### For Upload:
1. **Upload one document at a time** for large files
2. **Wait for "Processing complete"** before uploading next
3. **Keep PDFs under 10MB** when possible

---

## 🔧 Debugging Timeout Issues

If timeouts persist after fixes:

### Check 1: Ollama Performance
```powershell
# Test Ollama response time
ollama run llama2 "Hello"
```

If slow (>5 seconds), consider:
- Using faster model: `ollama pull phi`
- Upgrading hardware (more RAM/CPU)
- Using GPU acceleration if available

### Check 2: Document Count
```python
# In backend logs, look for:
"Current collection size: X documents"
```

If X > 50 documents:
- Increase timeouts further (add 30s per 50 docs)
- Implement pagination in dashboard
- Add document filters

### Check 3: Backend Logs
Watch the backend window for:
- "Processing query..." (should appear quickly)
- "Ollama response received" (LLM finished)
- Any ERROR or WARNING messages

---

## ✅ Success Criteria

After applying fixes, you should see:

✅ Dashboard loads within 2-3 minutes (first time)
✅ AI queries complete within 1-2 minutes
✅ Progress indicators show during loading
✅ Helpful error messages if timeout still occurs
✅ Retry attempts for transient failures

---

## 🆘 Still Having Issues?

If timeouts persist:

1. **Check these files exist**:
   - All documents properly uploaded?
   - ChromaDB collection populated?
   
2. **System resources**:
   - CPU usage during query? (Task Manager)
   - RAM available? (Should have 8GB+)
   - Disk space? (Embeddings take space)

3. **Network issues**:
   - Localhost slow? (Try 127.0.0.1)
   - Firewall blocking? (Allow Python)
   - Antivirus scanning? (Exclude AUREX folder)

---

## 📝 Summary

**Why Timeouts**: Backend processing + LLM inference takes time
**Quick Fix**: Increase all timeouts to 180-300 seconds
**Better Fix**: Add retry logic + progress indicators  
**Best Fix**: All above + backend caching

**Want me to apply these fixes automatically?** Just say "yes apply fixes"!
