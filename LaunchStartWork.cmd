@echo off
setlocal
set "SCRIPT_DIR=%~dp0"

where pythonw.exe >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw.exe "%SCRIPT_DIR%StartWorkApp.pyw"
    exit /b 0
)

where py.exe >nul 2>nul
if %errorlevel%==0 (
    start "" py.exe -3w "%SCRIPT_DIR%StartWorkApp.pyw"
    exit /b 0
)

where python.exe >nul 2>nul
if %errorlevel%==0 (
    python.exe "%SCRIPT_DIR%StartWorkApp.pyw"
    exit /b %errorlevel%
)

echo Python is not installed or is not added to PATH.
echo Install Python 3 from https://www.python.org/downloads/
echo During installation, enable "Add python.exe to PATH".
echo.
pause
exit /b 1
endlocal
