#!/bin/bash

echo "Conversation Evaluation Benchmark - Startup Script"
echo "=================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Running tests..."
python test_project.py

echo ""
echo "Starting API server..."
echo "The API will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"

cd src/api
python -m uvicorn main:app --reload --port 8000