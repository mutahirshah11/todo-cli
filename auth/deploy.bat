@echo off
echo Starting deployment of Authentication Service...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the service
echo Starting Authentication Service...
start /B python start_auth_service.py --port 8001

echo Authentication Service deployed successfully!
echo Access the service at: http://localhost:8001

pause