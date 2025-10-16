@echo off
REM ============================================================
REM   Task & Comment Management System - ONE-CLICK SETUP
REM   Double-click this file to set up EVERYTHING
REM ============================================================

cd /d "%~dp0"

echo.
echo ============================================================
echo   Task ^& Comment Management System
echo   COMPLETE AUTOMATED SETUP
echo ============================================================
echo.
echo This will install:
echo   - Python virtual environment
echo   - All backend dependencies (Flask, SQLAlchemy, pytest, etc.)
echo   - All frontend dependencies (React, TypeScript, etc.)
echo   - Initialize and seed database
echo   - Configure VS Code settings
echo.
echo Estimated time: 3-5 minutes
echo.
pause

echo.
echo Starting setup...
echo.

REM Check if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PowerShell not found!
    echo Please install PowerShell to run this setup.
    pause
    exit /b 1
)

REM Run the PowerShell setup script
powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   SETUP COMPLETED SUCCESSFULLY!
    echo ============================================================
    echo.
    echo Next steps:
    echo   1. Close this window
    echo   2. Double-click START.bat to run the application
    echo.
) else (
    echo.
    echo ============================================================
    echo   SETUP FAILED
    echo ============================================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
