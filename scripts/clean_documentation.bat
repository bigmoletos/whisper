@echo off
REM Cleans the generated documentation.

echo "Cleaning documentation..."
if exist ..\docs (
    rmdir /s /q ..\docs
)
echo "Done."
pause
