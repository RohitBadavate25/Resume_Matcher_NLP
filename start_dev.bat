@echo off
title ResumeMatch - AI-Powered Resume Matcher
color 0A

echo.
echo =====================================
echo   ResumeMatch Development Environment
echo =====================================
echo.
echo Starting AI-Powered Resume Matcher...
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo ERROR: Backend directory not found!
    echo Please make sure you're running this from the project root directory.
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo ERROR: Frontend directory not found!
    echo Please make sure you're running this from the project root directory.
    pause
    exit /b 1
)

echo [1/3] Checking Python virtual environment...
if not exist "backend\venv" (
    echo WARNING: Virtual environment not found in backend\venv
    echo Please run the setup first or check setup_instructions.md
    pause
)

echo [2/3] Starting Backend Server (Flask API)...
echo Backend will be available at: http://localhost:5000
start "ResumeMatch Backend" cmd /k "cd /d backend && if exist venv\Scripts\activate.bat (venv\Scripts\activate.bat) && python app.py"

echo.
echo [3/3] Waiting for backend to initialize...
timeout /t 8 /nobreak > nul

echo Starting Frontend Server (React App)...
echo Frontend will be available at: http://localhost:3000
start "ResumeMatch Frontend" cmd /k "cd /d frontend && npm start"

echo.
echo =====================================
echo   ResumeMatch is Starting Up!
echo =====================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000
echo.
echo The application will open automatically in your browser.
echo Both servers are starting in separate windows.
echo.
echo Close this window or press any key to continue...
pause > nul
