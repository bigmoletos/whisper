@echo off
REM Cleans the project from all the generated files.

echo "Cleaning the project..."
call .\clean.bat
call .\clean_documentation.bat
if exist ..\dist (
    rmdir /s /q ..\dist
)
if exist ..\build (
    rmdir /s /q ..\build
)
if exist ..\.pytest_cache (
    rmdir /s /q ..\.pytest_cache
)
if exist ..\Whisper_STT_Global_v1.0.zip (
    del ..\Whisper_STT_Global_v1.0.zip
)
echo "Done."
pause
