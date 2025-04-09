#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Run Flask development server
export FLASK_APP=src.app:app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000 