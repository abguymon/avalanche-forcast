#!/bin/bash

# Avalanche Forecast Dashboard Startup Script

echo "🏔️  Starting Avalanche Forecast Dashboard..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   or visit: https://github.com/astral-sh/uv"
    exit 1
fi

# Check if data file exists
if [ ! -f "allData.csv" ]; then
    echo "⚠️  Warning: allData.csv not found. The application may not work properly."
    echo "   Make sure your data file is in the project root directory."
    echo ""
fi

# Install dependencies and start the Flask application
echo "📦 Installing dependencies with uv..."
uv sync
echo ""

echo "🚀 Starting Flask application..."
echo "   Dashboard will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

uv run python app.py
