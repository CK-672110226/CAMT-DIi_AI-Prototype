# Windows batch file to set up and run the app
# Save this as setup.bat and run with: setup.bat

@echo off
cls
echo ======================================
echo Chihuahua vs Muffin Classifier Setup
echo ======================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Train model
echo Training model...
python train.py

REM Create uploads directory
if not exist uploads mkdir uploads

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To start the application:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate.bat
echo 2. Run the Flask app:
echo    python app.py
echo 3. Open in browser:
echo    http://localhost:5012
echo.
pause
