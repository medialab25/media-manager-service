@echo off

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

echo Setup complete! Virtual environment is ready.
echo To activate the virtual environment, run: venv\Scripts\activate.bat 