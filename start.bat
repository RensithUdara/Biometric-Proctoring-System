@echo off
echo Starting Biometric Proctoring System...
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Start the application
echo Starting the proctoring system...
python app.py

pause
