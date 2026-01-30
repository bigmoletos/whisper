@echo off
chcp 65001 >nul

echo ================================================
echo    Recréation environnement virtuel Python 3.12
echo ================================================
echo.

set "ROOT_DIR=%~dp0.."
set "VENV_DIR=%ROOT_DIR%\venv_whisper"

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    exit /b 1
)

echo [INFO] Python 3.12 détecté : 
py -3.12 --version
echo.

:: Supprimer l'ancien environnement virtuel si il existe
if exist "%VENV_DIR%" (
    echo [INFO] Suppression de l'ancien environnement virtuel...
    rmdir /s /q "%VENV_DIR%" 2>nul
    timeout /t 2 >nul
)

:: Créer le nouvel environnement virtuel avec Python 3.12
echo [INFO] Création du nouvel environnement virtuel avec Python 3.12...
py -3.12 -m venv "%VENV_DIR%"

if errorlevel 1 (
    echo [ERREUR] Échec de la création de l'environnement virtuel
    echo [INFO] Vérifiez les permissions et l'espace disque
    pause
    exit /b 1
)

echo [OK] Environnement virtuel créé avec succès

:: Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat"

:: Vérifier la version de Python dans le venv
echo [INFO] Version Python dans l'environnement virtuel :
python --version

:: Mettre à jour pip
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip

:: Installer les dépendances de base
echo [INFO] Installation des dépendances de base...
python -m pip install wheel setuptools

:: Installer les dépendances du projet
if exist "%ROOT_DIR%\requirements.txt" (
    echo [INFO] Installation des dépendances du projet...
    python -m pip install -r "%ROOT_DIR%\requirements.txt"
) else (
    echo [WARNING] Fichier requirements.txt non trouvé
)

:: Installer Faster-Whisper avec support CUDA
echo [INFO] Installation de Faster-Whisper...
python -m pip install faster-whisper

:: Installer PyTorch avec support CUDA
echo [INFO] Installation de PyTorch avec support CUDA...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo.
echo [OK] Installation terminée avec succès !
echo [INFO] Environnement virtuel Python 3.12 prêt à l'utilisation
echo.

:: Test rapide
echo [INFO] Test de l'installation...
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA disponible: {torch.cuda.is_available()}')"

echo.
pause