@echo off
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] .venv not found. Please run setup_env.bat first!
    pause
    exit /b 1
)

echo Starting FastAPI Backend at http://localhost:8000 ...
".venv\Scripts\uvicorn.exe" api_server:app --reload --port 8000
