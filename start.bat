@echo off
REM LinkedIn Profile Query Bot - Windows Startup Script

echo =====================================
echo   LinkedIn Profile Query Bot Startup
echo =====================================

REM Check for Python installation
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is required but not installed.
    exit /b 1
)

REM Check for virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to create virtual environment.
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    exit /b 1
)

REM Install dependencies if needed
if not exist venv\.dependencies_installed (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to install dependencies.
        exit /b 1
    )
    
    echo Installing spaCy language model...
    python -m spacy download en_core_web_sm
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to download spaCy language model.
        exit /b 1
    )
    
    REM Mark dependencies as installed
    echo. > venv\.dependencies_installed
)

REM Create profiles directory if it doesn't exist
if not exist profiles mkdir profiles

REM Check for .env file
if not exist .env (
    echo Warning: .env file not found. Creating from example...
    if exist .env.example (
        copy .env.example .env
        echo Please edit .env file with your configuration.
    ) else (
        echo Warning: .env.example not found. You'll need to create a .env file manually.
    )
)

REM Determine run mode
set MODE=all
if "%1"=="api" set MODE=api
if "%1"=="wati" set MODE=wati
if "%1"=="all" set MODE=all

REM Run the application
echo Starting LinkedIn Profile Query Bot in %MODE% mode...
python main.py --mode %MODE%

REM Deactivate virtual environment on exit
deactivate
