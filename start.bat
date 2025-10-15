@echo off
REM Avalanche Forecast Dashboard Startup Script for Windows

echo 🏔️  Starting Avalanche Forecast Dashboard...
echo.

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ uv is not installed. Please install uv first:
    echo    Visit: https://github.com/astral-sh/uv
    echo    Or run: pip install uv
    pause
    exit /b 1
)

REM Check if data file exists
if not exist allData.csv (
    echo ⚠️  Warning: allData.csv not found. The application may not work properly.
    echo    Make sure your data file is in the project root directory.
    echo.
)

REM Install dependencies and start the Flask application
echo 📦 Installing dependencies with uv...
uv sync
echo.

echo 🚀 Starting Flask application...
echo    Dashboard will be available at: http://localhost:5000
echo    Press Ctrl+C to stop the server
echo.

uv run python app.py
pause
