@echo off
REM Biometric Proctoring System Setup Script for Windows

echo ===================================
echo Biometric Proctoring System Setup
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or later.
    pause
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python requirements
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist "models\known_faces" mkdir models\known_faces
if not exist "reports" mkdir reports
if not exist "static" mkdir static
if not exist "templates" mkdir templates

echo ✓ Directories created

echo.
echo ===================================
echo Setup completed successfully! 🎉
echo ===================================
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the application: python app.py
echo 3. Open your browser to: http://localhost:5000
echo.
echo Before first use:
echo - Add known face images to models\known_faces\ folder
echo - Images should be named as: student_name.jpg
echo - Ensure good lighting and clear face visibility
echo.
echo Features available:
echo ✓ Real-time face recognition
echo ✓ Multiple person detection
echo ✓ Attention monitoring
echo ✓ Tab switching detection
echo ✓ Violation logging and reporting
echo ✓ Professional dashboard
echo ✓ PDF report generation
echo.

pause
