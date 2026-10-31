# How to See and Delete Duplicate Documents

## ✅ Problem Solved!

I've improved the Upload page so you can now:
1. **See all uploaded documents** clearly
2. **Identify duplicates** (marked with warning)
3. **Delete individual files** (one by one)
4. **Delete all files** (bulk delete)
5. **Search documents** (find specific files)

---

## 🚀 How to Use (After Restart)

### **Step 1: Restart Frontend**

The new features need frontend restart:

```powershell
# Kill frontend
taskkill /F /FI "WINDOWTITLE eq AUREX Frontend*"

# Wait 3 seconds
timeout /t 3

# Restart
cd "C:\Users\Sanika Naik\OneDrive\Desktop\MegaProject\AUREX"
venv\Scripts\activate
streamlit run frontend/streamlit_app.py
```

**OR just:**
```powershell
RESTART_AUREX.bat
```

---

### **Step 2: Go to Upload Page**

Open browser: http://localhost:8501/Upload

Scroll down to "📚 Uploaded Documents" section

---

### **Step 3: See Your Documents**

You'll now see something like:

```
📚 Uploaded Documents
[🔄 Refresh List] [🗑️ Delete All]

📊 Total documents: 19 | Click 🗑️ to delete duplicates

🔍 Search documents: [search box]

⚠️ Orders.xlsx - 2 copies found (DUPLICATE)
📄 Orders.xlsx (Copy 1)     XLSX    6.4 MB    ✅ completed    [🗑️ Delete]
📄 Orders.xlsx (Copy 2)     XLSX    6.4 MB    ✅ completed    [🗑️ Delete]

⚠️ Orders_2024.csv - 2 copies found (DUPLICATE)
📄 Orders_2024.csv (Copy 1)  CSV    5.7 MB    ✅ completed    [🗑️ Delete]
📄 Orders_2024.csv (Copy 2)  CSV    5.7 MB    ✅ completed    [🗑️ Delete]

... (more files)
```

---

## 🗑️ How to Delete Documents

### **Method 1: Delete Individual File**

1. Find the file you want to delete
2. Click the **[🗑️ Delete]** button next to it
3. Wait for "✅ Deleted!" message
4. File is removed immediately

### **Method 2: Delete All Duplicates**

1. Identify duplicates (marked with ⚠️)
2. Keep one copy, delete the others
3. Click [🗑️ Delete] on the duplicate copies
4. Keep one original

### **Method 3: Delete Everything (Start Fresh)**

1. Click **[🗑️ Delete All]** button at top
2. Warning appears: "⚠️ Click again to confirm"
3. Click **[🗑️ Delete All]** again to confirm
4. All documents deleted
5. Upload fresh files

### **Method 4: Search and Delete**

1. Type filename in search box: "Orders"
2. Shows only matching files
3. Delete the ones you don't want
4. Clear search to see all files again

---

## 🎯 Features Added

### **1. Duplicate Detection** ⚠️
- Groups files by filename
- Shows warning if multiple copies exist
- Labels each copy: (Copy 1), (Copy 2), etc.

### **2. Search Function** 🔍
- Search box at top of document list
- Type any part of filename
- Shows only matching documents
- Great for finding specific duplicates

### **3. Refresh Button** 🔄
- Manually refresh document list
- Useful after deleting files
- Ensures you see latest state

### **4. Bulk Delete** 🗑️
- Delete all documents at once
- Requires confirmation (click twice)
- Useful for starting completely fresh

### **5. Better Display** 📊
- Shows file type (PDF, CSV, XLSX)
- Shows file size in KB/MB
- Shows status (completed, processing, failed)
- Shows truncated document ID

### **6. Improved Timeouts** ⏱️
- Document list load: 30 seconds (was 5)
- Delete operation: 10 seconds (was 5)
- Better error messages if timeout

---

## 📋 Your Specific Situation

You uploaded files twice, so you have:

| Filename | Copies | Action |
|----------|--------|--------|
| Orders.xlsx | 2 | Keep 1, delete 1 |
| Orders_2024.csv | 2 | Keep 1, delete 1 |
| Products.xlsx | 2 | Keep 1, delete 1 |
| Regions.csv | 2 | Keep 1, delete 1 |
| Returns.csv | 2 | Keep 1, delete 1 |
| PDFs (various) | 9 copies | Keep what you need |

**Total**: 19 files → Should be ~10 after deleting duplicates

---

## 🎬 Step-by-Step: Clean Up Duplicates

### **Step 1: Restart AUREX**
```powershell
RESTART_AUREX.bat
```

### **Step 2: Go to Upload Page**
http://localhost:8501/Upload

### **Step 3: Scroll to Document List**
Look for "📚 Uploaded Documents"

### **Step 4: Identify Duplicates**
Files marked with ⚠️ are duplicates

### **Step 5: Delete Duplicates**
For each duplicate:
- Keep the first copy (Copy 1)
- Delete the second copy (Copy 2)
- Click [🗑️ Delete] button

### **Step 6: Verify**
- Click [🔄 Refresh List]
- Should now show ~10 files (no more duplicates)

### **Step 7: Done!**
Dashboard should now load faster with fewer files ✅

---

## 💡 Tips

### **To Find Specific Duplicate:**
```
1. Type filename in search: "Orders"
2. Shows only "Orders" files
3. Delete the duplicate
4. Clear search
```

### **To Start Completely Fresh:**
```
1. Click [🗑️ Delete All]
2. Click again to confirm
3. All files deleted
4. Upload only what you need
```

### **To Keep Documents Organized:**
```
- Don't upload same file twice
- Check Upload page before uploading
- Use search to find existing files
- Delete old versions before uploading new ones
```

---

## 🆘 Troubleshooting

### **Problem: Can't See Documents**

**Solution:**
```powershell
# Restart AUREX
RESTART_AUREX.bat

# Wait 20 seconds

# Go to Upload page
# Click [🔄 Refresh List]
# Wait 10-15 seconds
```

### **Problem: Delete Button Doesn't Work**

**Solution:**
- Check if backend is running (Backend window open?)
- Wait a moment and try again
- Check backend logs for errors
- Restart AUREX if needed

### **Problem: "Timeout loading documents"**

**Solution:**
- You have too many files (19 is a lot!)
- Wait 30 seconds and click Refresh
- Or delete some files using file explorer:
  ```powershell
  # Delete files manually
  del "data\raw\*.*"
  ```
- Then restart AUREX

---

## 🔧 What I Changed

### **File Modified:**
`frontend/pages/1_📤_Upload.py`

### **Changes Made:**
1. ✅ Increased document list timeout (5s → 30s)
2. ✅ Added duplicate detection and warnings
3. ✅ Added search functionality
4. ✅ Added refresh button
5. ✅ Added bulk delete (Delete All)
6. ✅ Better document display (size, type, ID)
7. ✅ Improved delete button (more visible)
8. ✅ Better error messages

---

## ✅ Summary

**Before Fix:**
- ❌ Couldn't see which files uploaded
- ❌ No way to identify duplicates
- ❌ Delete button was tiny (just 🗑️)
- ❌ Timeout loading document list

**After Fix:**
- ✅ See all files clearly
- ✅ Duplicates marked with ⚠️
- ✅ Big [🗑️ Delete] buttons
- ✅ Search to find specific files
- ✅ Delete All for bulk cleanup
- ✅ Longer timeout (works with 19 files)

---

**Restart AUREX and go to Upload page to see the improvements!** 🎉
