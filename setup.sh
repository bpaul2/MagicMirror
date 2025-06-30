#!/bin/bash

VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"

echo "Checking for existing virtual environment..."

if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists. Activating..."
else
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment. Ensure Python 3 is installed and in your PATH."
        exit 1
    fi
fi

source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

echo "Virtual environment activated"

if [ -f "$REQUIREMENTS" ]; then
    echo "Installing dependencies..."
    # python -m pip install --upgrade pip
    pip install -r "$REQUIREMENTS"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        deactivate
        exit 1
    fi
    echo "Dependencies installed"
else
    echo "No '$REQUIREMENTS' found. Skipping dependency installation"
fi

echo "Setup complete. You are now in the virtual environment"
echo "To exit the virtual environment, type 'deactivate'"