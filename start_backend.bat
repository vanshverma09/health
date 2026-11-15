@echo off
echo ====================================================
echo Starting DataVision Health Backend (FastAPI + ML)
echo ====================================================

cd /d "%~dp0backend"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in backend\.venv
    pause
    exit /b 1
)

echo Checking and seeding database...
.venv\Scripts\python.exe -m app.seed_data

echo.
echo Starting FastAPI server at http://127.0.0.1:8000
echo Interactive API Documentation available at http://127.0.0.1:8000/docs
echo.
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

pause

