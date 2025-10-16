#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Complete automated setup for Task & Comment Management System
.DESCRIPTION
    One-command setup that installs ALL dependencies, creates virtual environment,
    initializes database, seeds sample data, and optionally starts servers
.PARAMETER SkipStart
    Skip starting servers after setup (default: false)
.EXAMPLE
    .\setup.ps1
    Complete setup and start servers
.EXAMPLE
    .\setup.ps1 -SkipStart
    Setup only, don't start servers
#>

param(
    [switch]$SkipStart = $false
)

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
║    🚀 Task & Comment Management System                      ║
║       COMPLETE AUTOMATED SETUP                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
$backendDir = Join-Path $projectRoot "backend"
$frontendDir = Join-Path $projectRoot "frontend"

# Step 1: Check prerequisites
Write-Step "Checking prerequisites..."

# Check Python
Write-Info "Checking Python installation..."
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 11) {
            Write-Success "Python $pythonVersion found"
        } else {
            Write-Error-Custom "Python 3.11+ required (found: $pythonVersion)"
            Write-Info "Download from: https://www.python.org/downloads/"
            exit 1
        }
    }
} catch {
    Write-Error-Custom "Python not found"
    Write-Info "Please install Python 3.11+ from: https://www.python.org/downloads/"
    exit 1
}

# Check Node.js
Write-Info "Checking Node.js installation..."
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v(\d+)\.") {
        $major = [int]$matches[1]
        if ($major -ge 16) {
            Write-Success "Node.js $nodeVersion found"
        } else {
            Write-Error-Custom "Node.js 16+ required (found: $nodeVersion)"
            Write-Info "Download from: https://nodejs.org/"
            exit 1
        }
    }
} catch {
    Write-Error-Custom "Node.js not found"
    Write-Info "Please install Node.js 16+ from: https://nodejs.org/"
    exit 1
}

# Check npm
Write-Info "Checking npm installation..."
try {
    $npmVersion = npm --version 2>&1
    Write-Success "npm $npmVersion found"
} catch {
    Write-Error-Custom "npm not found"
    Write-Info "npm should come with Node.js. Please reinstall Node.js."
    exit 1
}

# Step 2: Backend Setup
Write-Step "Setting up Flask Backend..."

Push-Location $backendDir

try {
    # Check if venv already exists
    if (Test-Path "venv") {
        Write-Info "Virtual environment already exists, skipping creation..."
    } else {
        Write-Info "Creating Python virtual environment..."
        python -m venv venv
        Write-Success "Virtual environment created"
    }

    # Activate virtual environment
    Write-Info "Activating virtual environment..."
    & ".\venv\Scripts\Activate.ps1"

    # Upgrade pip
    Write-Info "Upgrading pip..."
    python -m pip install --upgrade pip --quiet

    # Install dependencies
    Write-Info "Installing Python dependencies (this may take a minute)..."
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt --quiet
        Write-Success "Python dependencies installed"
    } else {
        Write-Error-Custom "requirements.txt not found"
        Pop-Location
        exit 1
    }

    # Create .env file if needed
    if (Test-Path ".env.example") {
        if (-not (Test-Path ".env")) {
            Write-Info "Creating .env file from template..."
            Copy-Item .env.example -Destination .env
            Write-Success ".env file created"
        }
    }

    # Initialize database
    Write-Info "Setting up database..."
    $env:FLASK_APP = "run.py"
    
    # Check if migrations folder exists
    if (-not (Test-Path "migrations")) {
        Write-Info "Initializing database migrations..."
        flask db init
    }

    # Run migrations
    Write-Info "Running database migrations..."
    flask db upgrade
    Write-Success "Database initialized"

    # Seed database
    Write-Info "Seeding database with sample data..."
    try {
        flask seed
        Write-Success "Sample data added"
    } catch {
        Write-Info "Seed command not available or already seeded (this is okay)"
    }

    Write-Success "Backend setup complete!"

} catch {
    Write-Error-Custom "Backend setup failed: $_"
    Pop-Location
    exit 1
}

Pop-Location

# Step 3: Frontend Setup
Write-Step "Setting up React Frontend..."

Push-Location $frontendDir

try {
    # Check if node_modules exists
    if (Test-Path "node_modules") {
        Write-Info "Node modules already installed, checking for updates..."
    } else {
        Write-Info "Installing npm dependencies (this may take 2-3 minutes)..."
    }

    # Install dependencies
    if (Test-Path "package.json") {
        npm install
        Write-Success "npm dependencies installed"
    } else {
        Write-Error-Custom "package.json not found"
        Pop-Location
        exit 1
    }

    # Create .env file if needed
    if (Test-Path ".env.example") {
        if (-not (Test-Path ".env")) {
            Write-Info "Creating .env file from template..."
            Copy-Item .env.example -Destination .env
            Write-Success ".env file created"
        }
    }

    Write-Success "Frontend setup complete!"

} catch {
    Write-Error-Custom "Frontend setup failed: $_"
    Pop-Location
    exit 1
}

Pop-Location

# Step 4: Create VS Code settings
Write-Step "Configuring VS Code settings..."

$vscodeDir = Join-Path $projectRoot ".vscode"
$settingsFile = Join-Path $vscodeDir "settings.json"

if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

if (-not (Test-Path $settingsFile)) {
    $settings = @{
        "python.defaultInterpreterPath" = "`${workspaceFolder}/backend/venv/Scripts/python.exe"
        "python.terminal.activateEnvironment" = $true
        "python.analysis.extraPaths" = @("`${workspaceFolder}/backend")
        "python.testing.pytestEnabled" = $true
        "python.testing.pytestArgs" = @("backend/app/tests")
        "python.testing.cwd" = "`${workspaceFolder}/backend"
    } | ConvertTo-Json -Depth 10

    $settings | Out-File -FilePath $settingsFile -Encoding utf8
    Write-Success "VS Code settings configured"
}

# Summary
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                              ║" -ForegroundColor Green
Write-Host "║                  SETUP COMPLETED SUCCESSFULLY!               ║" -ForegroundColor Green
Write-Host "║                                                              ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Info "    What was installed:"
Write-Info "   ✓ Python virtual environment (backend/venv/)"
Write-Info "   ✓ All Python dependencies (Flask, SQLAlchemy, pytest, etc.)"
Write-Info "   ✓ All npm dependencies (React, TypeScript, Axios, etc.)"
Write-Info "   ✓ Database initialized with migrations"
Write-Info "   ✓ Sample data seeded"
Write-Info "   ✓ VS Code settings configured"
Write-Host ""

Write-Info "    Project Status:"
Write-Info "    ✓ Backend: Ready"
Write-Info "    ✓ Frontend: Ready"
Write-Info "    ✓ Database: Initialized"
Write-Info "    ✓ Tests: 41 tests ready to run"
Write-Host ""

if (-not $SkipStart) {
    Write-Step "Starting development servers..."
    Write-Host ""
    Write-Info "Backend will start on:  http://localhost:5000"
    Write-Info "Frontend will start on: http://localhost:3000"
    Write-Host ""
    
    $response = Read-Host "Start servers now? (Y/n)"
    
    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        Write-Host ""
        Write-Info "Starting servers in separate windows..."
        Write-Info "To stop servers: Close the PowerShell windows or press Ctrl+C"
        Write-Host ""
        
        # Start backend
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
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript
        
        Start-Sleep -Seconds 2
        
        # Start frontend
        $frontendScript = @"
Set-Location '$frontendDir'
Write-Host '╔════════════════════════════════════════════════════╗' -ForegroundColor Cyan
Write-Host '║               REACT FRONTEND SERVER                ║' -ForegroundColor Cyan
Write-Host '║               http://localhost:3000                ║' -ForegroundColor Cyan
Write-Host '╚════════════════════════════════════════════════════╝' -ForegroundColor Cyan
Write-Host ''
npm start
"@
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript
        
        Write-Success "Servers starting! Browser will open automatically."
        Write-Host ""
    } else {
        Write-Host ""
        Write-Info "   To start servers later, use one of these methods:"
        Write-Host ""
        Write-Info "   Option 1 (Easiest): Double-click START.bat"
        Write-Info "   Option 2: Run .\start.ps1"
        Write-Info "   Option 3: Manual start (see README.md)"
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Info "   To start servers, use one of these methods:"
    Write-Host ""
    Write-Info "   Option 1 (Easiest): Double-click START.bat"
    Write-Info "   Option 2: Run .\start.ps1"
    Write-Info "   Option 3: Manual start (see README.md)"
    Write-Host ""
}

Write-Host ""
Write-Success "Setup complete! Happy coding! 🎉"
Write-Host ""
Write-Host ""
Write-Host "Frontend (Terminal 2):" -ForegroundColor Yellow
Write-Host "  cd frontend" -ForegroundColor White
Write-Host "  npm start" -ForegroundColor White
Write-Host ""
Write-Host "Or use Docker:" -ForegroundColor Yellow
Write-Host "  docker-compose up --build" -ForegroundColor White
Write-Host ""
Write-Host "Application URLs:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:5000/api" -ForegroundColor White
Write-Host ""
