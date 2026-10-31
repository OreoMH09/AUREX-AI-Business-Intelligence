# AUREX - Super Simple Start Guide

## 🚀 How to Start AUREX (3 Steps!)

### Step 1: Double-click this file
```
START_AUREX.bat
```

### Step 2: Wait 20 seconds
Two windows will open. Keep them open!

### Step 3: Open browser
```
http://localhost:8501
```

**Done!** ✅

---

## 🔄 How to Start AUREX Again (Next Time)

### Same 3 steps:

1. Double-click `START_AUREX.bat`
2. Wait 20 seconds
3. Open http://localhost:8501

**That's it!** Every time the same! 🎯

---

## ⚠️ If You See Error

### Use this instead:
```
RESTART_AUREX.bat
```

**Then:**
1. Wait 20 seconds
2. Open http://localhost:8501

---

## 🛑 How to Stop AUREX

### Just close the 2 terminal windows

Or run:
```powershell
taskkill /F /IM python.exe /T
```

---

## 📝 About CSV Upload Issue

### CSV Upload Tips:

1. **File Encoding**: Save CSV as UTF-8
   - Excel → "Save As" → Select "CSV UTF-8"

2. **Column Names**: Keep them simple
   - ✅ Good: "Revenue", "Date", "Amount"
   - ❌ Bad: "Revenue $$$", "Date/Time", "Amount (USD)"

3. **File Size**: Keep under 5MB
   - Large CSV? Split into smaller files

4. **Test First**: Try uploading a simple CSV:
   ```
   Name,Value
   Item1,100
   Item2,200
   ```

### If CSV Upload Fails:

**Error might be**:
- Encoding issue (file not UTF-8)
- Special characters in data
- Empty rows at end
- Column headers missing

**Quick Fix**:
1. Open CSV in Excel
2. "Save As" → "CSV UTF-8 (Comma delimited)"
3. Try uploading again

---

## ✅ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't start | Run `RESTART_AUREX.bat` |
| Connection error | Wait 30 seconds, refresh browser |
| Timeout error | Normal for first load, wait 1 minute |
| CSV fails | Save as UTF-8 encoding |
| Port busy | Run `taskkill /F /IM python.exe /T` |

---

## 🎯 Remember These 3 Files:

1. **START_AUREX.bat** - Start AUREX ✅
2. **RESTART_AUREX.bat** - Fix problems ✅
3. **http://localhost:8501** - Open this in browser ✅

---

## 💡 One More Time (Super Clear!)

### To Start AUREX:
```
1. Double-click: START_AUREX.bat
2. Wait: 20 seconds
3. Open: http://localhost:8501
```

### To Stop AUREX:
```
Close the 2 terminal windows
```

### To Restart AUREX:
```
1. Double-click: RESTART_AUREX.bat
2. Wait: 20 seconds  
3. Open: http://localhost:8501
```

---

**That's all you need to know!** 🎉

**For detailed guide, see**: `HOW_TO_START_AUREX.md`
