#!/bin/bash

echo "🚀 Deploying Sustainable Skies Streamlit Application"
echo "=================================================="

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Installing Streamlit..."
    pip install streamlit
fi

# Install all requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Launch the application
echo "🌍 Launching Sustainable Skies Dashboard..."
echo "Application will open in your default browser"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --server.port 8501 --server.address localhost

echo "✅ Application stopped"
