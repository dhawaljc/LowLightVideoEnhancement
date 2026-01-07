#!/bin/bash

echo "================================================"
echo "Low-Light Video Enhancement - Quick Start"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Creating necessary directories..."
mkdir -p uploads outputs static

echo ""
echo "================================================"
echo "Setup complete!"
echo "================================================"
echo ""
echo "To start the server, run:"
echo "  python app.py"
echo ""
echo "Then open your browser and navigate to:"
echo "  http://localhost:5000"
echo ""
echo "================================================"
