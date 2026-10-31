# Fix: Documents Not Deleting Properly

## Current Status

You have **10 files** remaining in `data/raw` folder:
1. Regions.csv
2. sample_business_report_2025.pdf
3. Annual_Report_2024.pdf
4. Orders_2024.csv
5. Annual_Report_2025.pdf
6. Customers.csv
7. Management_Report.pdf
8. Products.xlsx
9. Orders.xlsx
10. Returns.csv

**This means deletion IS working!** You went from 19 → 10 files.

## Why They Still Show in Upload Page

### Possible Causes:

### 1. **Backend Memory Out of Sync** (Most Likely)
- You deleted files from disk ✅
- Backend memory still has old 19 documents ❌
- Upload page shows what's in memory, not on disk

**Solution:** Restart AUREX to re-sync
```powershell
RESTART_AUREX.bat
```

### 2. **Browser Cache**
- Upload page cached old data
- Refresh not clearing cache

**Solution:** Hard refresh
```
Ctrl + Shift + R  (Chrome/Edge)
or
Ctrl + F5
```

### 3. **Delete Didn't Complete**
- Delete API call succeeded
- But file deletion failed
- Or vector store deletion failed

**Solution:** Check backend logs for errors

### 4. **Deleted Documents Re-appear After Restart**
- Documents deleted from memory
- Files still on disk
- Restart re-discovers them

**This should NOT happen** - your delete function removes files from disk.

## Verification Steps

### Step 1: Check Files on Disk
```powershell
dir data\raw /B
```

Should show **10 files** (not 19).

### Step 2: Check Backend Memory
```powershell
VERIFY_DELETION.bat
```

Shows:
- Files on disk: X
- Documents in memory: Y

If X ≠ Y, restart needed!

### Step 3: Check Upload Page
1. Go to http://localhost:8501/Upload
2. Click "🔄 Refresh List" button
3. Count documents shown

Should show **10 documents** (matching disk).

## Complete Fix Process

### Fix 1: Restart to Re-sync ✅

```powershell
# Stop AUREX
taskkill /F /IM python.exe /T

# Start AUREX
START_AUREX.bat
```

Backend will:
1. Discover files in data/raw (10 files)
2. Register in memory (10 documents)
3. Upload page will show 10 documents ✅

### Fix 2: Hard Refresh Browser ✅

After restart:
1. Go to Upload page
2. Press **Ctrl + Shift + R** (hard refresh)
3. Or clear browser cache
4. Count documents again

### Fix 3: Clear ChromaDB if Needed ✅

If deleted documents still appear in dashboard:

```powershell
# Stop AUREX first
taskkill /F /IM python.exe /T

# Delete ChromaDB folder
rmdir /S /Q data\chroma_db

# Start AUREX (will recreate ChromaDB)
START_AUREX.bat
```

This forces complete re-ingestion of only the 10 remaining files.

## Expected Results After Fix

### Upload Page:
```
📚 Uploaded Documents
📊 Total documents: 10

Documents:
1. ✅ Regions.csv
2. ✅ sample_business_report_2025.pdf
3. ✅ Annual_Report_2024.pdf
4. ✅ Orders_2024.csv
5. ✅ Annual_Report_2025.pdf
6. ✅ Customers.csv
7. ✅ Management_Report.pdf
8. ✅ Products.xlsx
9. ✅ Orders.xlsx
10. ✅ Returns.csv
```

No duplicates! ✅

### Backend Console:
```
INFO: Discovered 10 existing documents
INFO: Starting background auto-ingestion thread for 10 documents
```

Only 10 documents processed (not 19).

### Dashboard:
Analytics based on 10 files only.

## Why Deletion Works Now

The `delete_document()` function:

```python
def delete_document(self, document_id: str) -> bool:
    # 1. Delete file from disk
    file_path.unlink()  ✅
    
    # 2. Delete from ChromaDB
    vector_store.delete_document(document_id)  ✅
    
    # 3. Remove from memory
    del self.documents[document_id]  ✅
```

All 3 steps execute properly!

## Troubleshooting

### If documents still show as 19:

**Problem:** Backend memory not synced with disk

**Solution:**
```powershell
RESTART_AUREX.bat
```

### If deleted files re-appear:

**Problem:** Files weren't actually deleted from disk

**Solution:** Manually check and delete
```powershell
# List files
dir data\raw

# Delete specific file
del "data\raw\{document_id}_{filename}"
```

### If Upload page frozen:

**Problem:** Frontend stuck on old data

**Solution:**
```powershell
# Stop frontend
taskkill /F /IM streamlit.exe

# Restart (only frontend)
cd frontend
streamlit run streamlit_app.py --server.port 8501
```

### If ChromaDB has ghost documents:

**Problem:** Deleted from disk but not from vector store

**Solution:** Clear and rebuild ChromaDB
```powershell
taskkill /F /IM python.exe /T
rmdir /S /Q data\chroma_db
START_AUREX.bat
```

## Quick Commands

### Check What's Actually There:
```powershell
VERIFY_DELETION.bat
```

### Force Re-sync:
```powershell
RESTART_AUREX.bat
```

### Hard Refresh Browser:
```
Ctrl + Shift + R
```

### Clear ChromaDB:
```powershell
rmdir /S /Q data\chroma_db
```

## Summary

✅ **Deletion IS working** - You have 10 files (down from 19)  
✅ **Just restart AUREX** - Will re-discover only 10 files  
✅ **Upload page will show 10** - No more duplicates  
✅ **Processing faster** - Only 10 files to ingest (~1.5 min vs 3 min)  

**Just run `RESTART_AUREX.bat` and everything syncs correctly!** 🎉
