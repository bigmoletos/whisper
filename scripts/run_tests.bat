@echo off
REM Runs the tests.

echo "Running tests..."
call ..\venv_whisper\Scripts\activate.bat
pytest ..\tests
echo "Done."
pause
