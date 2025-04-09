@echo off

:: Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the service in direct mode
call manage.sh start

:: Show logs
call manage.sh logs 