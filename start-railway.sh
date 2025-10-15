#!/bin/bash

# Railway startup script
echo "🏔️ Starting Avalanche Forecast on Railway..."

# Set default port if not provided
export PORT=${PORT:-5000}

# Start the application
echo "🚀 Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 wsgi:app
