#!/bin/bash

# Biometric Proctoring System Setup Script

echo "==================================="
echo "Biometric Proctoring System Setup"
echo "==================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "✓ Python found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install system dependencies (Ubuntu/Debian)
if command -v apt-get &> /dev/null; then
    echo "Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y cmake build-essential libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev python3-dev
fi

# Install Python requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p models/known_faces
mkdir -p reports
mkdir -p static
mkdir -p templates

echo "✓ Directories created"

# Set permissions (Unix-like systems)
if [[ "$OSTYPE" != "msys" && "$OSTYPE" != "win32" ]]; then
    chmod +x app.py
    echo "✓ Permissions set"
fi

echo ""
echo "==================================="
echo "Setup completed successfully! 🎉"
echo "==================================="
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: python app.py"
echo "3. Open your browser to: http://localhost:5000"
echo ""
echo "Before first use:"
echo "- Add known face images to models/known_faces/ folder"
echo "- Images should be named as: student_name.jpg"
echo "- Ensure good lighting and clear face visibility"
echo ""
echo "Features available:"
echo "✓ Real-time face recognition"
echo "✓ Multiple person detection"
echo "✓ Attention monitoring"
echo "✓ Tab switching detection"
echo "✓ Violation logging and reporting"
echo "✓ Professional dashboard"
echo "✓ PDF report generation"
echo ""
