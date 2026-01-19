@echo off
REM Generates the documentation using Sphinx.

echo "Generating documentation..."
call ..\venv_whisper\Scripts\activate.bat
pip install sphinx
sphinx-quickstart ..\docs --quiet -p "Whisper STT Global" -a "Bigmoletos" -v "1.0" -r "" -l "en"
sphinx-apidoc -o ..\docs\source ..\src
cd ..\docs
make html
cd ..\scripts
echo "Done."
pause
