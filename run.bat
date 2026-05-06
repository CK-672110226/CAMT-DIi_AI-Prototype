@echo off
REM Script to start the Flask application on Windows

cls
echo ======================================
echo Starting Chihuahua vs Muffin Classifier
echo ======================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Running setup.bat...
    call setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if model exists
if not exist image_classifier_model.h5 (
    echo Model not found. Training model...
    python train.py
)

REM Start the application
echo Starting Flask application...
echo Access the app at: http://localhost:5012
echo.
python app.py

pause
