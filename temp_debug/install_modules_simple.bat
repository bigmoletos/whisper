@echo off
chcp 65001 >nul

echo ================================================
echo    INSTALLATION MODULES PYTHON 3.12 (MODE USER)
echo ================================================
echo.

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis
    pause
    exit /b 1
)
echo [OK] Python 3.12 détecté

:: Mise à jour pip
echo.
echo [1/8] Mise à jour de pip...
py -3.12 -m pip install --user --upgrade pip

:: Installation PyTorch avec CUDA
echo.
echo [2/8] Installation PyTorch avec CUDA...
py -3.12 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

:: Installation NumPy
echo.
echo [3/8] Installation NumPy...
py -3.12 -m pip install --user numpy

:: Installation SoundDevice
echo.
echo [4/8] Installation SoundDevice...
py -3.12 -m pip install --user sounddevice

:: Installation Faster-Whisper
echo.
echo [5/8] Installation Faster-Whisper...
py -3.12 -m pip install --user faster-whisper

:: Installation Whisper standard (fallback)
echo.
echo [6/8] Installation Whisper standard...
py -3.12 -m pip install --user openai-whisper

:: Installation PyAutoGUI
echo.
echo [7/8] Installation PyAutoGUI...
py -3.12 -m pip install --user pyautogui

:: Installation autres dépendances
echo.
echo [8/8] Installation autres dépendances...
py -3.12 -m pip install --user keyboard pyperclip pywin32

echo.
echo [SUCCESS] Installation terminée !
echo [INFO] Testez maintenant avec: test_modules.bat
echo.
pause