@echo off
title Chess Coach - Setup
cd /d "%~dp0"

echo ========================================
echo       Chess Coach - One-Click Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo [OK] Python %pyver% found

REM Check Stockfish
if not exist "stockfish.exe" (
    echo [INFO] Stockfish not found in current directory.
    echo Download from: https://stockfishchess.org/download/
    echo Place stockfish.exe in this folder and re-run setup.
) else (
    echo [OK] Stockfish found
)

REM Create virtual environment if not exists
if not exist ".venv" (
    echo [..] Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

REM Activate and install dependencies
echo [..] Installing dependencies...
call .venv\Scripts\activate.bat

pip install --upgrade pip -q
pip install -r requirements.txt -q

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

echo [OK] All dependencies installed
echo.

echo ========================================
echo        Setup complete!
echo ========================================
echo.
echo To run the app:
echo   python run.py          - Desktop mode
echo   python run.py web      - Web mode
echo.
pause
