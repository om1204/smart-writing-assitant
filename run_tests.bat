@echo off
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] .venv not found. Please run setup_env.bat first!
    pause
    exit /b 1
)

echo ==========================================================
echo Running NLP Pipeline Test Suite (Tests 1 to 10)
echo ==========================================================
".venv\Scripts\python.exe" tests\test_all_10_samples.py
echo.
pause
