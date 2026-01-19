@echo off
REM Packages the application into a single executable file using PyInstaller.

echo "Packaging the application..."

REM Create a dummy icon if it doesn't exist
if not exist ..\icon.ico (
    echo "Creating a dummy icon.ico file..."
    (
        echo [Desktop]
        echo IconFile=shell32.dll
        echo IconIndex=20
    ) > ..\icon.ico
)

call ..\venv_whisper\Scripts\activate.bat
pyinstaller --onefile --windowed --name WhisperSTT --icon=..\icon.ico ..\src\main.py
echo "Done."
pause