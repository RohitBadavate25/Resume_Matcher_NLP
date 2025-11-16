@echo off
title ResumeMatch Setup
color 0B

echo.
echo =====================================
echo      ResumeMatch Setup Script
echo =====================================
echo.
echo This script will set up the ResumeMatch application
echo on your Windows machine.
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org/downloads/
    pause
    exit /b 1
)

REM Check Node.js installation
echo [2/6] Checking Node.js installation...
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js 14+ from https://nodejs.org/
    pause
    exit /b 1
)

echo Python and Node.js are installed ✓
echo.

REM Setup Backend
echo [3/6] Setting up Python backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install requirements
echo Installing Python dependencies...
call venv\Scripts\activate.bat
if exist "requirements.txt" (
    pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Python dependencies!
        pause
        exit /b 1
    )
) else (
    echo ERROR: requirements.txt not found!
    pause
    exit /b 1
)

echo [4/6] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True)"

echo [5/6] Installing spaCy English model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo WARNING: spaCy model installation failed. The app will still work with reduced NLP capabilities.
)

REM Create uploads directory
if not exist "uploads" (
    mkdir uploads
)

cd ..

REM Setup Frontend
echo [6/6] Setting up React frontend...
cd frontend

if exist "package.json" (
    echo Installing Node.js dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Node.js dependencies!
        pause
        exit /b 1
    )
) else (
    echo ERROR: package.json not found!
    pause
    exit /b 1
)

cd ..

echo.
echo =====================================
echo        Setup Complete! ✓
echo =====================================
echo.
echo ResumeMatch has been successfully set up!
echo.
echo To start the application:
echo   1. Double-click start_dev.bat, or
echo   2. Run: start_dev.bat from command line
echo.
echo The application will be available at:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5000
echo.
echo For detailed instructions, see setup_instructions.md
echo.
echo Press any key to exit...
pause > nul
