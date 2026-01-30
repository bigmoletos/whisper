@echo off
chcp 65001 >nul

echo ================================================
echo    CONFIGURATION VTT AVEC PYTHON 3.12
echo ================================================
echo.

:: Répertoire du projet
set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%venv_whisper"

:: Vérifier Python 3.12
echo [INFO] Vérification de Python 3.12...
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé. Versions disponibles :
    py -0 2>nul
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    exit /b 1
)

for /f "delims=" %%i in ('py -3.12 -c "import sys; print(sys.version)"') do echo [OK] Python 3.12 détecté: %%i

:: Supprimer complètement l'ancien environnement virtuel
if exist "%VENV_DIR%" (
    echo [INFO] Suppression de l'ancien environnement virtuel...
    
    :: Tenter de désactiver d'abord
    if exist "%VENV_DIR%\Scripts\deactivate.bat" (
        call "%VENV_DIR%\Scripts\deactivate.bat" 2>nul
    )
    
    :: Attendre un peu
    timeout /t 2 >nul
    
    :: Supprimer avec force
    rmdir /s /q "%VENV_DIR%" 2>nul
    
    :: Vérifier si supprimé
    if exist "%VENV_DIR%" (
        echo [WARNING] Suppression partielle. Continuons...
    ) else (
        echo [OK] Ancien environnement supprimé
    )
)

:: Créer un nouvel environnement virtuel avec Python 3.12
echo [INFO] Création d'un nouvel environnement virtuel avec Python 3.12...
py -3.12 -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ERREUR] Échec de création de l'environnement virtuel
    pause
    exit /b 1
)

echo [OK] Environnement virtuel créé

:: Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERREUR] Échec de l'activation
    pause
    exit /b 1
)

:: Vérifier la version de Python dans le venv
echo [INFO] Vérification de la version Python dans l'environnement virtuel...
python --version
if errorlevel 1 (
    echo [ERREUR] Python non fonctionnel dans l'environnement virtuel
    pause
    exit /b 1
)

:: Mettre à jour pip
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip

:: Installer les dépendances essentielles
echo [INFO] Installation des dépendances essentielles...
python -m pip install wheel setuptools

:: Installer PyTorch avec CUDA
echo [INFO] Installation de PyTorch avec support CUDA...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

:: Installer Whisper et Faster-Whisper
echo [INFO] Installation de Whisper et Faster-Whisper...
python -m pip install openai-whisper faster-whisper

:: Installer les dépendances audio
echo [INFO] Installation des dépendances audio...
python -m pip install sounddevice numpy scipy

:: Installer les dépendances système Windows
echo [INFO] Installation des dépendances système Windows...
python -m pip install pyautogui keyboard pyperclip python-dotenv pywin32

:: Test final
echo [INFO] Test de l'installation...
python -c "
import sys
import torch
import whisper
import faster_whisper
import sounddevice

print('=== TEST INSTALLATION PYTHON 3.12 ===')
print('Python version:', sys.version)
print('Whisper: OK')
print('Faster-Whisper: OK')
print('PyTorch version:', torch.__version__)
print('CUDA disponible:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU:', torch.cuda.get_device_name(0))
print('SoundDevice: OK')
print('=== INSTALLATION REUSSIE ===')
"

if errorlevel 1 (
    echo [ERREUR] Test d'installation échoué
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Configuration Python 3.12 terminée avec succès !
echo [INFO] Vous pouvez maintenant utiliser Voice-to-Text Turbo
echo [INFO] Utilisez le menu principal (start.bat) option 2
echo.
pause