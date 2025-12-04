@echo off
echo ========================================
echo  🚀 Starting GitReadme (Gemini Version)
echo ========================================

REM --- 🔥 BACKEND SETUP ---
IF NOT EXIST venv (
    echo [Backend] Creating fresh virtual environment...
    python -m venv venv
)

echo [Backend] Activating venv...
call venv\Scripts\activate

echo [Backend] Installing Dependencies...
pip install --upgrade pip
cd backend
pip install -r requirements.txt
cd ..

echo [Backend] Starting FastAPI...
start cmd /k "call venv\Scripts\activate && cd backend && uvicorn fastapi_app:app --reload"

REM --- 🔥 FRONTEND SETUP ---
cd gitreadme-frontend

IF NOT EXIST node_modules (
    echo [Frontend] Installing dependencies...
    npm install
)

echo [Frontend] Starting Next.js UI...
start cmd /k "npm run dev"
cd ..

echo ========================================
echo  Backend → http://localhost:8000/docs
echo  Frontend → http://localhost:3000
echo ========================================
pause
