@echo off
REM One-Click Startup for Task & Comment Management System
REM Double-click this file to start both servers

cd /d "%~dp0"

echo.
echo ============================================================
echo   Task ^& Comment Management System - Quick Start
echo ============================================================
echo.

REM Check if setup was done
if not exist "backend\venv" (
    echo ERROR: Project not set up yet!
    echo Please run setup.ps1 first.
    echo.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not installed!
    echo Please run setup.ps1 first.
    echo.
    pause
    exit /b 1
)

echo Starting servers...
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Close the server windows to stop them.
echo.

REM Start backend in new window
start "Flask Backend (Port 5000)" powershell -NoExit -Command "cd '%~dp0backend'; Write-Host 'FLASK BACKEND SERVER' -ForegroundColor Cyan; Write-Host 'http://localhost:5000' -ForegroundColor Green; Write-Host ''; & '.\venv\Scripts\Activate.ps1'; python run.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "React Frontend (Port 3000)" powershell -NoExit -Command "cd '%~dp0frontend'; Write-Host 'REACT FRONTEND SERVER' -ForegroundColor Cyan; Write-Host 'http://localhost:3000' -ForegroundColor Green; Write-Host ''; npm start"

echo.
echo ============================================================
echo   Servers are starting!
echo ============================================================
echo.
echo You can close this window safely.
echo The servers will continue running in their own windows.
echo.
echo Press any key to exit...
pause >nul
