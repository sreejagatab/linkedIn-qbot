#!/bin/bash
# LinkedIn Profile Query Bot - Startup Script

# Display banner
echo "====================================="
echo "  LinkedIn Profile Query Bot Startup"
echo "====================================="

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo "Error: Failed to activate virtual environment."; exit 1; }

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies."
        exit 1
    fi
    
    echo "Installing spaCy language model..."
    python -m spacy download en_core_web_sm
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download spaCy language model."
        exit 1
    fi
    
    # Mark dependencies as installed
    touch venv/.dependencies_installed
fi

# Create profiles directory if it doesn't exist
mkdir -p profiles

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Please edit .env file with your configuration."
    else
        echo "Warning: .env.example not found. You'll need to create a .env file manually."
    fi
fi

# Determine run mode
MODE="all"
if [ "$1" == "api" ] || [ "$1" == "wati" ] || [ "$1" == "all" ]; then
    MODE="$1"
fi

# Run the application
echo "Starting LinkedIn Profile Query Bot in $MODE mode..."
python main.py --mode $MODE

# Deactivate virtual environment on exit
deactivate
