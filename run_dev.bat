@echo off

:: Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set Flask environment variables
set FLASK_APP=src.app:app
set FLASK_ENV=development

:: Run Flask development server
flask run --host=0.0.0.0 --port=5000 