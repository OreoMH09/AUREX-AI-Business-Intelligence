@echo off
echo ========================================
echo   AUREX - AI Business Intelligence
echo ========================================
echo.
echo Starting AUREX system...
echo.

REM Start backend in a new window
echo [1/2] Starting Backend Server...
start "AUREX Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && set PYTHONPATH=%CD% && python app/main.py"

REM Wait for backend to start (increased time)
echo Waiting for backend to initialize...
timeout /t 8 /nobreak > nul

REM Start frontend in a new window
echo [2/2] Starting Frontend UI...
start "AUREX Frontend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && set PYTHONPATH=%CD% && streamlit run frontend/streamlit_app.py"

echo.
echo ========================================
echo   AUREX Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:8501
echo API Docs: http://localhost:8000/api/docs
echo.
echo Two windows opened:
echo   1. Backend Server (FastAPI)
echo   2. Frontend UI (Streamlit)
echo.
echo Wait a few seconds, then refresh your browser!
echo.
echo Close those windows to stop AUREX.
echo.
pause
