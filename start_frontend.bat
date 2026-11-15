@echo off
echo ====================================================
echo Starting DataVision Health Frontend (React + Vite)
echo ====================================================

cd /d "%~dp0frontend"

echo.
echo Launching React Clinical Dashboard on http://localhost:5173
echo.
npm run dev

pause

