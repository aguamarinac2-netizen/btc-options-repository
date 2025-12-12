#!/bin/bash

echo "================================================"
echo "  BTCUSDT Options Trading System"
echo "  AI-Powered Semi-Automated Trading Dashboard"
echo "================================================"
echo ""

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the btc_options_trader directory"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if dependencies are installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo ""
    echo "⚠️  Dependencies not installed. Installing now..."
    pip install -r requirements.txt
    echo ""
fi

# Check if config exists
if [ ! -f "config/credentials.json.example" ]; then
    echo "❌ Error: Config file not found at config/credentials.json.example"
    exit 1
fi

echo "✓ Configuration found"
echo ""

# Display warning
echo "⚠️  RISK WARNING ⚠️"
echo "Options trading involves significant risk."
echo "Never invest more than you can afford to lose."
echo ""
echo "This is a SEMI-AUTOMATED system."
echo "YOU must manually approve all trades."
echo ""

# Countdown
echo "Starting dashboard in 3 seconds..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1

# Launch the dashboard
echo ""
echo "🚀 Launching dashboard..."
echo "📊 Dashboard will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the system"
echo "================================================"
echo ""

streamlit run main.py
