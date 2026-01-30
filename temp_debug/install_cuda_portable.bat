@echo off
echo ========================================
echo   INSTALLATION CUDA PORTABLE (Sans Admin)
echo ========================================
echo.
echo Ce script installe CUDA via Conda sans droits admin
echo.

cd /d "%~dp0\.."

echo [INFO] Verification de l'environnement...

REM Verifier si conda/miniconda est installe
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVERTISSEMENT] Conda non detecte
    echo.
    echo Options disponibles:
    echo 1. Installer Miniconda portable (recommande)
    echo 2. Utiliser l'installation manuelle
    echo.
    choice /c 12 /m "Choisissez une option"
    if errorlevel 2 goto manual_install
    if errorlevel 1 goto install_miniconda
)

:install_cuda_conda
echo [INFO] Installation de CUDA via Conda...
echo.

REM Creer un environnement dedie pour CUDA
echo [INFO] Creation de l'environnement CUDA...
conda create -n cuda_env python=3.10 -y

echo [INFO] Activation de l'environnement...
call conda activate cuda_env

echo [INFO] Installation des packages CUDA...
conda install -c conda-forge cudatoolkit=11.8 -y
conda install -c conda-forge cudnn -y

echo [INFO] Installation de PyTorch avec CUDA...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo [INFO] Test de l'installation CUDA...
python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}'); print(f'Version CUDA: {torch.version.cuda}'); print(f'Nombre de GPU: {torch.cuda.device_count()}')"

goto end

:install_miniconda
echo [INFO] Telechargement de Miniconda portable...
echo.
echo Veuillez telecharger Miniconda depuis:
echo https://docs.conda.io/en/latest/miniconda.html
echo.
echo Choisissez la version Windows x86_64 et installez dans:
echo %USERPROFILE%\miniconda3
echo.
echo Puis relancez ce script.
pause
goto end

:manual_install
echo [INFO] Installation manuelle de CUDA...
echo.
echo METHODE 1: CUDA Portable
echo 1. Telechargez CUDA Toolkit depuis:
echo    https://developer.nvidia.com/cuda-downloads
echo 2. Choisissez "exe (network)" au lieu de "exe (local)"
echo 3. Lancez avec: cuda_installer.exe -s -extract:C:\temp\cuda
echo 4. Copiez les fichiers vers votre dossier utilisateur
echo.
echo METHODE 2: Via pip (plus simple)
echo pip install nvidia-cuda-runtime-cu11
echo pip install nvidia-cuda-nvcc-cu11
echo.
pause

:end
echo.
echo [INFO] Installation terminee
echo.
echo Pour utiliser CUDA avec Whisper:
echo 1. Activez l'environnement: conda activate cuda_env
echo 2. Installez faster-whisper: pip install faster-whisper
echo 3. Modifiez config.json: "device": "cuda"
echo.
pause