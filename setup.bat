@echo off
echo ================================
echo Gmail Unsubscriber - Setup
echo ================================
echo.
echo This will install everything you need.
echo.
pause

echo.
echo Step 1: Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo Python found!

echo.
echo Step 2: Installing required packages...
echo This may take a minute...
echo.

python -m pip install --upgrade pip
python -m pip install google-auth-oauthlib==1.2.0
python -m pip install google-auth-httplib2==0.2.0
python -m pip install google-api-python-client==2.108.0

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install packages
    echo.
    echo Try running Command Prompt as Administrator:
    echo 1. Press Windows key
    echo 2. Type "cmd"
    echo 3. Right-click Command Prompt
    echo 4. Click "Run as administrator"
    echo 5. Run this setup.bat file again
    echo.
    pause
    exit /b 1
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Get your credentials.json file (see WINDOWS_SETUP.md)
echo 2. Double-click run.bat to scan your emails
echo.
pause
