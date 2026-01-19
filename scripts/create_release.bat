@echo off
REM Creates a release zip file of the project.

echo "Creating release zip file..."
tar -acf ..\Whisper_STT_Global_v1.0.zip ..\* --exclude=../.git --exclude=../.vscode --exclude=../venv_whisper --exclude=../build --exclude=../dist --exclude=../docs/_build --exclude=../.pytest_cache --exclude=../src/__pycache__ --exclude=../Whisper_STT_Global_v1.0.zip
echo "Done."
pause
