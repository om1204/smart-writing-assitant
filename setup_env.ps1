Write-Host "=========================================================="
Write-Host "Setting up Python Virtual Environment..."
Write-Host "=========================================================="

$PYTHON_EXE = "python"

Write-Host "[1/3] Creating virtual environment (.venv)..."
& $PYTHON_EXE -m venv .venv

Write-Host "[2/3] Installing dependencies from requirements.txt..."
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\pip.exe" install -r requirements.txt

Write-Host "[3/3] Setting permissions on .venv..."
icacls ".venv" /grant "*S-1-15-2-1:(OI)(CI)RX" /T | Out-Null

Write-Host "=========================================================="
Write-Host "Running all 10 tests..."
Write-Host "=========================================================="
& ".\.venv\Scripts\python.exe" tests\test_all_10_samples.py
