@echo off
echo ========================================
echo   INSTALLATION CUDA VIA PIP (Sans Admin)
echo ========================================
echo.

cd /d "%~dp0\.."

echo [INFO] Activation de l'environnement virtuel...
if exist "venv_whisper\Scripts\activate.bat" (
    call venv_whisper\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouve
    echo Executez d'abord install.bat
    pause
    exit /b 1
)

echo [INFO] Mise a jour de pip...
python -m pip install --upgrade pip

echo [INFO] Installation des packages CUDA via pip...
echo.

REM Installation des runtime CUDA
echo [INFO] Installation CUDA Runtime...
pip install nvidia-cuda-runtime-cu11
pip install nvidia-cuda-nvcc-cu11
pip install nvidia-cublas-cu11
pip install nvidia-cufft-cu11
pip install nvidia-curand-cu11
pip install nvidia-cusolver-cu11
pip install nvidia-cusparse-cu11
pip install nvidia-cudnn-cu11

echo [INFO] Installation de PyTorch avec support CUDA...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo [INFO] Installation de faster-whisper optimise...
pip install faster-whisper

echo [INFO] Test de l'installation...
python scripts\utils\test_cuda_installation.py

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] CUDA installe et teste avec succes
) else if %errorlevel% equ 1 (
    echo.
    echo [WARNING] Installation partielle - certains composants manquent
) else (
    echo.
    echo [ERROR] Echec de l'installation CUDA
)

echo.
echo [INFO] Installation terminee
echo.
echo PROCHAINES ETAPES:
echo 1. Modifiez projects/voice-to-text-turbo/config.json
echo 2. Changez "device": "cpu" vers "device": "cuda"
echo 3. Testez avec start-voice-turbo.bat
echo.
pause