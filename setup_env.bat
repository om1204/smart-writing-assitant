@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo Setting up Python Virtual Environment...
echo ==========================================================

set "PYTHON_EXE=python"

echo [1/3] Creating virtual environment (.venv)...
%PYTHON_EXE% -m venv .venv

echo [2/3] Installing dependencies from requirements.txt...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\pip.exe" install -r requirements.txt
".venv\Scripts\python.exe" -m spacy download en_core_web_sm

echo [3/3] Setting permissions on .venv...
icacls ".venv" /grant "*S-1-15-2-1:(OI)(CI)RX" /T >nul 2>&1

echo ==========================================================
echo Running all 10 tests...
echo ==========================================================
".venv\Scripts\python.exe" tests\test_all_10_samples.py

pause
