@echo off
setlocal EnableDelayedExpansion

REM Change directory to the script location
cd /d "%~dp0"

REM Check if an argument is provided (drag and drop)
if not "%~1"=="" (
    REM Convert Windows path to WSL path
    for /f "usebackq delims=" %%A in (`wsl wslpath -u "%~1"`) do set "TARGET_DIR=%%A"
    echo Target Directory: %~1
    echo WSL Path: !TARGET_DIR!
    echo.
    
    REM Run the python script with the target directory
    REM Use bash -l -c to ensure environment variables are loaded
    wsl bash -l -c "uv run main.py \"!TARGET_DIR!\""
) else (
    REM If no argument, run for the current directory
    echo Target Directory: Current Directory
    echo.
    wsl bash -l -c "uv run main.py"
)

echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Filenames copied to clipboard.
) else (
    echo [ERROR] An error occurred.
)

echo.
echo Press any key to exit...
pause >nul
