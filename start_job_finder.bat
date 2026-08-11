@echo off
title Launching Personal AI Job Finder...
echo ====================================================
echo Starting Personal AI Job Finder Stack...
echo ====================================================

:: Launch Backend FastAPI server in a new window
start "AI Job Finder Backend" cmd /k "cd /d %~dp0backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

:: Launch Frontend Next.js app in a new window
start "AI Job Finder Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are launching!
echo Backend API: http://localhost:8000
echo Frontend Dashboard: http://localhost:3000
echo ====================================================
timeout /t 5
start http://localhost:3000
