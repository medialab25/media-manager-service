#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete! Virtual environment is ready."
echo "To activate the virtual environment, run: source venv/bin/activate" 