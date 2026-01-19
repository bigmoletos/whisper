@echo off
REM Deletes the __pycache__ directory.

echo "Cleaning..."
if exist ..\src\__pycache__ (
    rmdir /s /q ..\src\__pycache__
)
echo "Done."
pause
