@echo off
chcp 65001 >nul

echo ================================================
echo    CORRECTION CUBLAS DLL MANQUANTE
echo ================================================
echo.

echo [INFO] Correction de l'erreur: cublas64_12.dll is not found
echo [INFO] Installation de CUDA Toolkit 12.x compatible
echo.

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis
    pause
    exit /b 1
)

:: Désinstaller l'ancienne version PyTorch
echo [1/4] Désinstallation de l'ancienne version PyTorch...
py -3.12 -m pip uninstall -y torch torchvision torchaudio

:: Installer PyTorch avec CUDA 12.1 (compatible avec cublas64_12.dll)
echo [2/4] Installation PyTorch avec CUDA 12.1...
py -3.12 -m pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

:: Installer NVIDIA CUDA Toolkit Runtime (sans admin)
echo [3/4] Installation CUDA Runtime Libraries...
py -3.12 -m pip install --user nvidia-cublas-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12

:: Test de la correction
echo [4/4] Test de la correction...
py -3.12 -c "
import torch
print('[INFO] PyTorch version:', torch.__version__)
print('[INFO] CUDA disponible:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('[INFO] GPU:', torch.cuda.get_device_name(0))
    
try:
    import faster_whisper
    model = faster_whisper.WhisperModel('tiny', device='cuda', compute_type='float16')
    print('[SUCCESS] Faster-Whisper avec CUDA fonctionne !')
    del model
except Exception as e:
    print('[ERREUR] Faster-Whisper CUDA:', e)
    print('[INFO] Utilisez le mode fallback (option 2)')
"

echo.
if errorlevel 1 (
    echo [WARNING] Correction partielle - utilisez l'option [2] (Mode Fallback)
) else (
    echo [SUCCESS] Correction réussie ! Vous pouvez maintenant utiliser l'option [1]
)
echo.
pause