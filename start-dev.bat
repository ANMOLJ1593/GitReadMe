@echo off
echo ========================================
echo   Starting GitReadme Project (Backend + Frontend)
echo ========================================

REM Start Backend
echo [Backend] Creating virtual environment...
python -m venv venv

echo [Backend] Activating virtual environment...
call venv\Scripts\activate

echo [Backend] Installing dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo [Backend] Starting FastAPI server...
start cmd /k "call venv\Scripts\activate && cd backend && uvicorn fastapi_app:app --reload"

REM Start Frontend
echo [Frontend] Installing dependencies...
cd gitreadme-frontend
npm install

echo [Frontend] Starting Next.js development server...
start cmd /k "npm run dev"

cd ..
echo ========================================
echo Both backend and frontend are now running.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
pause
