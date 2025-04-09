@echo off

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install development dependencies
pip install -r requirements.txt

:: Install pre-commit hooks
pre-commit install

echo Setup complete! Virtual environment is ready.
echo To activate the virtual environment, run: venv\Scripts\activate.bat 