@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pythonw.exe "%SCRIPT_DIR%StartWorkApp.pyw"
if errorlevel 1 python "%SCRIPT_DIR%StartWorkApp.pyw"
endlocal
