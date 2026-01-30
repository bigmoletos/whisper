@echo off
chcp 65001 >nul

echo ================================================
echo    CORRECTION COMPLÈTE CUDA POUR FASTER-WHISPER
echo ================================================
echo.

echo [INFO] Correction de l'erreur cublas64_12.dll pour accélération GPU
echo [INFO] Installation complète CUDA 12.x compatible
echo.

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis
    pause
    exit /b 1
)
echo [OK] Python 3.12 détecté

:: Nettoyage complet
echo.
echo [1/6] Nettoyage des anciennes installations...
py -3.12 -m pip uninstall -y torch torchvision torchaudio
py -3.12 -m pip uninstall -y nvidia-cublas-cu11 nvidia-cudnn-cu11 nvidia-cufft-cu11
py -3.12 -m pip uninstall -y nvidia-cublas-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12

:: Installation PyTorch CUDA 12.1
echo.
echo [2/6] Installation PyTorch avec CUDA 12.1...
py -3.12 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

:: Installation bibliothèques NVIDIA CUDA 12
echo.
echo [3/6] Installation bibliothèques NVIDIA CUDA 12...
py -3.12 -m pip install --user nvidia-cublas-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12 nvidia-curand-cu12 nvidia-cusolver-cu12 nvidia-cusparse-cu12

:: Réinstallation Faster-Whisper
echo.
echo [4/6] Réinstallation Faster-Whisper...
py -3.12 -m pip uninstall -y faster-whisper
py -3.12 -m pip install --user faster-whisper

:: Test PyTorch CUDA
echo.
echo [5/6] Test PyTorch CUDA...
py -3.12 scripts\test_cuda_pytorch.py pytorch

if errorlevel 1 (
    echo [ERREUR] PyTorch CUDA ne fonctionne pas
    pause
    exit /b 1
)

:: Test Faster-Whisper avec CUDA
echo.
echo [6/6] Test Faster-Whisper avec CUDA...
py -3.12 scripts\test_cuda_pytorch.py faster-whisper

if errorlevel 1 (
    echo.
    echo [ERREUR] Faster-Whisper CUDA ne fonctionne pas
    echo [INFO] Vérifiez que vos drivers NVIDIA sont à jour
    pause
    exit /b 1
)

echo.
echo ================================================
echo    CORRECTION CUDA RÉUSSIE !
echo ================================================
echo [SUCCESS] CUDA 12.x installé et fonctionnel
echo [SUCCESS] Faster-Whisper avec GPU opérationnel
echo [SUCCESS] Vous pouvez maintenant utiliser l'option [1] avec accélération GPU
echo.
echo [INFO] Testez avec: start.bat puis choisir [1]
echo.
pause