@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║                      🤖 Baby AGI UI 🤖                    ║
echo ║                                                           ║
echo ║                  Web Interface Starting...               ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 📡 Starting web server...
echo 🌐 Open your browser to: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

python -m baby_agi.web_server
pause
