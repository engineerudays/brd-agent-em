#!/bin/bash
# Quick start script for BRD Agent UI

echo "🚀 Starting BRD Agent UI..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if backend is running
if ! curl -s http://localhost:5678 > /dev/null; then
    echo "⚠️  Warning: n8n backend (port 5678) is not reachable"
    echo "   Make sure to start the backend with: docker-compose up -d"
    echo ""
fi

# Start Streamlit
echo "📱 Opening UI at http://localhost:8501"
echo ""
streamlit run app.py

