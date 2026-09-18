@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo Setting up Python 3.11 Virtual Environment with uv...
echo ==========================================================

REM Locate Python 3.11
set "PYTHON_311=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_311%" (
    set "PYTHON_311=python"
)

REM Grant AppContainer permissions so IDE can access python & uv
icacls "%LOCALAPPDATA%\Programs\Python" /grant "*S-1-15-2-1:(OI)(CI)RX" /T >nul 2>&1
icacls "%USERPROFILE%\.local" /grant "*S-1-15-2-1:(OI)(CI)RX" /T >nul 2>&1

REM Locate uv
where uv >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set UV_EXE=uv
) else if exist "%USERPROFILE%\.local\bin\uv.exe" (
    set UV_EXE="%USERPROFILE%\.local\bin\uv.exe"
) else (
    set UV_EXE=uv
)

echo [1/3] Creating virtual environment (.venv) using Python 3.11...
%UV_EXE% venv .venv --python "%PYTHON_311%" --allow-existing

echo [2/3] Installing dependencies from requirements.txt via uv...
%UV_EXE% pip install -r requirements.txt --python ".venv\Scripts\python.exe"

echo [3/3] Setting permissions on .venv...
icacls ".venv" /grant "*S-1-15-2-1:(OI)(CI)RX" /T >nul 2>&1

echo ==========================================================
echo Running all 10 tests...
echo ==========================================================
".venv\Scripts\python.exe" tests\test_all_10_samples.py

pause
