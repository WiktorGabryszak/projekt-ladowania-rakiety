@echo off
echo ============================================================
echo    SYMULATOR LADOWANIA RAKIETY - WERSJA WEB
echo ============================================================
echo.

REM Sprawdz czy Flask jest zainstalowany
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalowanie wymaganych pakietow...
    pip install flask flask-cors
    echo.
)

echo Uruchamianie serwera...
echo Otworz przegladarke: http://localhost:5000
echo.
echo Aby zatrzymac serwer, nacisnij Ctrl+C
echo ============================================================
echo.

python web_app.py

pause
