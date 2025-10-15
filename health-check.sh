#!/bin/bash

# Health check script for the Avalanche Forecast application
echo "🏔️  Avalanche Forecast Health Check"
echo "=================================="

# Check if the application is running
if curl -f http://localhost:5000/api/data > /dev/null 2>&1; then
    echo "✅ Application is healthy and running"
    echo "🌐 Dashboard: http://localhost:5000"
    echo "📊 API: http://localhost:5000/api/data"
    
    # Get basic stats
    echo ""
    echo "📈 Current Statistics:"
    curl -s http://localhost:5000/api/data | python3 -m json.tool
else
    echo "❌ Application is not responding"
    echo "🔧 Try restarting with: docker-compose restart"
    exit 1
fi
