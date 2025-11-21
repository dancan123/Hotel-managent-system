@echo off

echo Installing backend dependencies...
pip install -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed successfully.

echo Creating PostgreSQL database if not exists...
psql -U your_username -h localhost -p 5432 -d postgres -c "SELECT 'CREATE DATABASE hotel_management' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hotel_management')\gexec"
if %errorlevel% neq 0 (
    echo Warning: Could not create database. Ensure PostgreSQL is running and credentials are correct.
)

echo Initializing database tables...
python -c "from backend.app import app, db; with app.app_context(): db.create_all()"
if %errorlevel% neq 0 (
    echo Failed to initialize database tables.
    pause
    exit /b 1
)
echo Database tables initialized.

echo Starting backend Flask server...
start python backend\app.py

echo Starting frontend HTTP server on port 8000...
start python -m http.server 8000 --directory frontend

echo Opening browser to frontend...
start http://localhost:8000

echo Startup complete. Backend running on http://localhost:5000, Frontend on http://localhost:8000

pause