#!/bin/bash
echo "========================================================"
echo "       CampusFind Portal - BCA College Project"
echo "========================================================"
echo ""
echo "[1/3] Seeding Database..."
cd backend
python3 seed.py

echo ""
echo "[2/3] Starting Flask Backend on Port 5000..."
python3 app.py &
BACKEND_PID=$!

echo ""
echo "[3/3] Starting React Vite Frontend on Port 5173..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================================"
echo " CampusFind is running!"
echo " Backend:  http://127.0.0.1:5000"
echo " Frontend: http://localhost:5173"
echo ""
echo " Demo Logins:"
echo "  - Admin:   admin@campusfind.edu / admin123"
echo "  - Student: aarav@student.edu    / student123"
echo "========================================================"
echo "Press CTRL+C to terminate both servers."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM EXIT
wait
