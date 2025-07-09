@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Launch Flask app in background
start "" python app.py
echo 🚀 Flask app launched...

:: Wait briefly to ensure server is running
timeout /t 3 > nul

:: Test /search endpoint using curl
echo 🔍 Checking ICD search for query: "bite"
curl http://127.0.0.1:5000/search?q=bite > test_output.html

IF EXIST test_output.html (
    echo ✅ Response saved to test_output.html
    echo Opening test_output.html...
    start test_output.html
) ELSE (
    echo ❌ Failed to retrieve response. Check app.py or server logs.
)

ENDLOCAL
EXIT /B 0
