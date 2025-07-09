@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Timestamp
FOR /F %%I IN ('wmic os get localdatetime ^| find "."') DO SET TS=%%I
SET TS=[%TS:~4,2%/%TS:~6,2%/%TS:~0,4% %TS:~8,2%:%TS:~10,2%:%TS:~12,2%]

:: Log setup
echo %TS% 🚀 Starting ICD Search App...

:: Install dependencies (silent)
pip install -r requirements.txt > NUL 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Failed to install dependencies.
    EXIT /B 1
) ELSE (
    echo ✅ Dependencies installed.
)

:: Launch the app
start "" python app.py
echo %TS% ✅ Flask app launched. Check terminal for LAN IP.

ENDLOCAL
EXIT /B 0
