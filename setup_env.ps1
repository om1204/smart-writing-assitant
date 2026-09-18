# Setup script for LexiFlow NLP Assistant using uv with Python 3.11
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Setting up Python 3.11 Virtual Environment with uv..." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$py311 = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (-not (Test-Path $py311)) {
    $py311 = "python"
}

# Step 1: Grant permissions
Write-Host "[1/3] Setting directory permissions for IDE access..." -ForegroundColor Yellow
try {
    if (Test-Path "$env:LOCALAPPDATA\Programs\Python") {
        icacls "$env:LOCALAPPDATA\Programs\Python" /grant "*S-1-15-2-1:(OI)(CI)RX" /T | Out-Null
    }
    if (Test-Path "$env:USERPROFILE\.local") {
        icacls "$env:USERPROFILE\.local" /grant "*S-1-15-2-1:(OI)(CI)RX" /T | Out-Null
    }
} catch { }

# Step 2: Locate uv
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if ($uvCmd) {
    $uvExe = $uvCmd.Source
} elseif (Test-Path "$env:USERPROFILE\.local\bin\uv.exe") {
    $uvExe = "$env:USERPROFILE\.local\bin\uv.exe"
} else {
    $uvExe = "uv"
}

# Step 3: Create .venv with Python 3.11
Write-Host "[2/3] Creating virtual environment using Python 3.11..." -ForegroundColor Yellow
& $uvExe venv .venv --python $py311 --allow-existing

# Step 4: Install requirements
Write-Host "[3/3] Installing dependencies with uv pip install..." -ForegroundColor Yellow
& $uvExe pip install -r requirements.txt --python ".venv\Scripts\python.exe"

# Re-apply permissions on .venv
if (Test-Path ".venv") {
    icacls ".venv" /grant "*S-1-15-2-1:(OI)(CI)RX" /T | Out-Null
}

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Setup Completed! Running Test Suite..." -ForegroundColor Green
& ".venv\Scripts\python.exe" tests\test_all_10_samples.py
