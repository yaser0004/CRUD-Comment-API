#!/usr/bin/env pwsh
<#
.SYNOPSIS
    One-click startup script for Task & Comment Management System
.DESCRIPTION
    Starts both backend (Flask) and frontend (React) development servers
    Use this after initial setup is complete (run setup.ps1 first)
.EXAMPLE
    .\start.ps1
#>

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
function Write-Info { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Error-Custom { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }
function Write-Step { param($msg) Write-Host "`n===> $msg" -ForegroundColor Yellow }

# Banner
Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        Task & Comment Management System - START SERVERS      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
$backendDir = Join-Path $projectRoot "backend"
$frontendDir = Join-Path $projectRoot "frontend"

# Check if project is set up
Write-Step "Checking project setup..."

# Check if virtual environment exists
$venvPath = Join-Path $backendDir "venv"
if (-not (Test-Path $venvPath)) {
    Write-Error-Custom "Virtual environment not found!"
    Write-Info "Please run setup.ps1 first to initialize the project."
    Write-Info "Usage: .\setup.ps1"
    exit 1
}
Write-Success "Virtual environment found"

# Check if node_modules exists
$nodeModulesPath = Join-Path $frontendDir "node_modules"
if (-not (Test-Path $nodeModulesPath)) {
    Write-Error-Custom "Node modules not found!"
    Write-Info "Please run setup.ps1 first to initialize the project."
    Write-Info "Usage: .\setup.ps1"
    exit 1
}
Write-Success "Node modules found"

# Check if database exists
$dbPath = Join-Path $backendDir "instance\app.db"
if (-not (Test-Path $dbPath)) {
    Write-Info "Database not initialized. Initializing now..."
    Push-Location $backendDir
    try {
        & ".\venv\Scripts\Activate.ps1"
        flask db upgrade
        Write-Success "Database initialized"
    } catch {
        Write-Error-Custom "Failed to initialize database: $_"
        Pop-Location
        exit 1
    }
    Pop-Location
}
Write-Success "Database ready"

Write-Host ""
Write-Info "╔═══════════════════════════════════════════════════════════╗"
Write-Info "║  Starting servers...                                      ║"
Write-Info "║                                                           ║"
Write-Info "║  Backend:  http://localhost:5000                          ║"
Write-Info "║  Frontend: http://localhost:3000                          ║"
Write-Info "║                                                           ║"
Write-Info "║  Press Ctrl+C in this window to stop all servers         ║"
Write-Info "╚═══════════════════════════════════════════════════════════╝"
Write-Host ""

# Start backend server in new window
Write-Step "Starting Flask backend server..."
$backendScript = @"
Set-Location '$backendDir'
Write-Host '╔════════════════════════════════════════════════════╗' -ForegroundColor Cyan
Write-Host '║               FLASK BACKEND SERVER                 ║' -ForegroundColor Cyan
Write-Host '║               http://localhost:5000                ║' -ForegroundColor Cyan
Write-Host '╚════════════════════════════════════════════════════╝' -ForegroundColor Cyan
Write-Host ''
& '.\venv\Scripts\Activate.ps1'
python run.py
"@
$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -PassThru
Write-Success "Backend server starting (PID: $($backendJob.Id))"

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start frontend server in new window
Write-Step "Starting React frontend server..."
$frontendScript = @"
Set-Location '$frontendDir'
Write-Host '╔════════════════════════════════════════════════════╗' -ForegroundColor Cyan
Write-Host '║               REACT FRONTEND SERVER                ║' -ForegroundColor Cyan
Write-Host '║               http://localhost:3000                ║' -ForegroundColor Cyan
Write-Host '╚════════════════════════════════════════════════════╝' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Starting development server...' -ForegroundColor Yellow
Write-Host ''
npm start
"@
$frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -PassThru
Write-Success "Frontend server starting (PID: $($frontendJob.Id))"

Write-Host ""
Write-Success "Both servers are starting!"
Write-Host ""
Write-Info "   Server Information:"
Write-Info "   Backend PID:  $($backendJob.Id)"
Write-Info "   Frontend PID: $($frontendJob.Id)"
Write-Host ""
Write-Info "   Access URLs:"
Write-Info "   Backend API:  http://localhost:5000"
Write-Info "   Frontend App: http://localhost:3000"
Write-Host ""
Write-Info "   Tips:"
Write-Info "   • Frontend will open automatically in your browser"
Write-Info "   • Backend logs visible in Flask window"
Write-Info "   • Frontend logs visible in React window"
Write-Host ""
Write-Info "   To stop servers:"
Write-Info "   • Close both PowerShell windows, or"
Write-Info "   • Press Ctrl+C in each window"
Write-Host ""
Write-Success "Setup complete! Happy coding! 🎉"
Write-Host ""

# Wait for user to press Ctrl+C
Write-Host "Press Ctrl+C to stop monitoring and exit this script..." -ForegroundColor Yellow
Write-Host "(Note: Servers will continue running in their own windows)" -ForegroundColor Yellow
Write-Host ""

try {
    # Keep script running to show status
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Info "Script terminated. Servers are still running in separate windows."
    Write-Info "Close the server windows to stop them."
}
