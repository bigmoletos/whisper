@echo off
REM Uninstalls the application.

echo "Uninstalling the application..."
echo "This will remove all the files and directories created by the application, except for the config.json file."
set /p continue="Are you sure you want to continue? (Y/N): "
if /i not "%continue%"=="Y" (
    exit /b 1
)

REM Remove the venv directory
if exist ..\venv_whisper (
    rmdir /s /q ..\venv_whisper
)

REM Remove the dist directory
if exist ..\dist (
    rmdir /s /q ..\dist
)

REM Remove the build directory
if exist ..\build (
    rmdir /s /q ..\build
)

REM Remove the __pycache__ directory
if exist ..\src\__pycache__ (
    rmdir /s /q ..\src\__pycache__
)

REM Remove the whisper_stt.log file
if exist ..\whisper_stt.log (
    del ..\whisper_stt.log
)

REM Remove the icon.ico file
if exist ..\icon.ico (
    del ..\icon.ico
)

REM Remove the .pytest_cache directory
if exist ..\.pytest_cache (
    rmdir /s /q ..\.pytest_cache
)

REM Remove the tests directory
if exist ..\tests (
    rmdir /s /q ..\tests
)

echo "Uninstallation complete."
pause
