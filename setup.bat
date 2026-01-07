@echo off
echo ================================================
echo Low-Light Video Enhancement - Quick Start
echo ================================================
echo.

echo Checking Python version...
python --version

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "static" mkdir static

echo.
echo ================================================
echo Setup complete!
echo ================================================
echo.
echo To start the server, run:
echo   python app.py
echo.
echo Then open your browser and navigate to:
echo   http://localhost:5000
echo.
echo ================================================
pause
