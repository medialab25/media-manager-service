#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

echo "Setup complete! Virtual environment is ready."
echo "To activate the virtual environment, run: source venv/bin/activate" 