@echo off
echo ============================================
echo   AUREX - RESTART (Clean Start)
echo ============================================
echo.

echo [Step 1/3] Stopping all Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Done!
echo.

echo [Step 2/3] Killing processes on ports 8000 and 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do taskkill /F /PID %%a >nul 2>&1
timeout /t 2 /nobreak >nul
echo Done!
echo.

echo [Step 3/3] Starting AUREX fresh...
echo.

REM Start backend in a new window
echo Starting Backend Server (Port 8000)...
start "AUREX Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && set PYTHONPATH=%CD% && python app/main.py"

REM Wait for backend to start
echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak > nul

REM Start frontend in a new window
echo Starting Frontend UI (Port 8501)...
start "AUREX Frontend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && set PYTHONPATH=%CD% && streamlit run frontend/streamlit_app.py"

echo.
echo ============================================
echo   AUREX Restarted Successfully!
echo ============================================
echo.
echo Two new windows should open:
echo   1. AUREX Backend (black window)
echo   2. AUREX Frontend (streamlit window)
echo.
echo Wait 15-20 seconds, then open:
echo   Frontend: http://localhost:8501
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/api/docs
echo.
echo If you see errors in the Backend window, press any key here
echo and I'll help you fix them!
echo.
pause
