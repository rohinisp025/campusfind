@echo off
title CampusFind - Lost and Found Portal
echo ========================================================
echo        CampusFind Portal - BCA College Project
echo ========================================================
echo.
echo [1/3] Checking Python and Node.js environments...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

echo.
echo [2/3] Initializing and Seeding SQLite Database...
cd backend
python seed.py
if %errorlevel% neq 0 (
    echo [ERROR] Database seeding encountered an issue.
    pause
    exit /b
)

echo.
echo [3/3] Starting Backend (Port 5000) and Frontend (Port 5173)...
start "CampusFind Flask Backend" cmd /k "python app.py"
cd ..\frontend
start "CampusFind React Frontend" cmd /k "npm.cmd run dev"

echo.
echo ========================================================
echo  CampusFind is launching!
echo  Backend:  http://127.0.0.1:5000
echo  Frontend: http://localhost:5173
echo.
echo  Demo Credentials:
echo   - Admin:   admin@campusfind.edu / admin123
echo   - Student: aarav@student.edu    / student123
echo ========================================================
timeout /t 3 >nul
start http://localhost:5173
pause
