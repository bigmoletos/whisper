@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ================================================
echo    VOICE-TO-TEXT TURBO - Transcription Rapide
echo    (Faster-Whisper - GPU/CUDA)
echo ================================================
echo.

:: Répertoire du projet
set "PROJECT_DIR=%~dp0"
set "ROOT_DIR=%PROJECT_DIR%..\.."
set "SHARED_DIR=%ROOT_DIR%\shared"
set "VENV_DIR=%ROOT_DIR%\venv_whisper"

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé. Veuillez installer Python 3.12+
    pause
    exit /b 1
)

:: Vérifier CUDA via PyTorch (plus fiable)
echo [INFO] Vérification de CUDA...
py -3.12 -c "import torch; print('[INFO] CUDA détecté' if torch.cuda.is_available() else '[AVERTISSEMENT] CUDA non détecté')" 2>nul
if errorlevel 1 (
    echo [AVERTISSEMENT] CUDA non détecté. L'application fonctionnera en mode CPU.
    echo [INFO] Pour de meilleures performances, installez CUDA Toolkit.
) else (
    echo [INFO] CUDA détecté - Mode GPU activé
)

:: Vérifier et créer/réparer l'environnement virtuel
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Activation de l'environnement virtuel...
    call "%VENV_DIR%\Scripts\activate.bat"

    :: Vérifier si pip fonctionne
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [AVERTISSEMENT] Environnement virtuel corrompu détecté
        echo [INFO] Suppression et recréation de l'environnement virtuel...
        call deactivate 2>nul
        rmdir /s /q "%VENV_DIR%"
        py -3.12 -m venv "%VENV_DIR%"
        call "%VENV_DIR%\Scripts\activate.bat"
    )
) else (
    echo [INFO] Création de l'environnement virtuel avec Python 3.12...
    py -3.12 -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
)

:: Vérifier si les dépendances sont installées
echo [DEBUG] Vérification des dépendances...
python -c "import sounddevice" >nul 2>&1
if errorlevel 1 (
    echo [INFO] sounddevice manquant
    set DEPS_MISSING=1
) else (
    echo [DEBUG] sounddevice OK
)

python -c "import faster_whisper" >nul 2>&1
if errorlevel 1 (
    echo [INFO] faster_whisper manquant
    set DEPS_MISSING=1
) else (
    echo [DEBUG] faster_whisper OK
)

if defined DEPS_MISSING (
    echo [INFO] Installation des dépendances requises...
    python -m pip install --upgrade pip
    python -m pip install -r "%ROOT_DIR%\requirements.txt"
    python -m pip install faster-whisper
    if errorlevel 1 (
        echo [ERREUR] Échec de l'installation des dépendances
        pause
        exit /b 1
    )
    echo [OK] Dépendances installées avec succès
) else (
    echo [DEBUG] Toutes les dépendances sont présentes
)

:: Forcer l'utilisation de la configuration du projet
echo [INFO] Configuration du projet Voice-to-Text Turbo...
copy "%PROJECT_DIR%config.json" "%SHARED_DIR%\src\config.json" >nul
if exist "%SHARED_DIR%\src\config.json" (
    echo [INFO] Configuration Turbo activée (CUDA + large-v3)
) else (
    echo [WARNING] Échec de copie de configuration
)

:: Lancer l'application
echo.
echo [INFO] Démarrage de Voice-to-Text Turbo...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo [DEBUG] Répertoire de travail: %SHARED_DIR%\src
echo [DEBUG] Configuration: %PROJECT_DIR%config.json
echo.

cd /d "%SHARED_DIR%\src"
echo [DEBUG] Lancement de: python main.py --config "%PROJECT_DIR%config.json"
python main.py --config "%PROJECT_DIR%config.json"

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur (code: %errorlevel%)
    echo [DEBUG] Vérifiez les logs ci-dessus pour plus de détails
    pause
) else (
    echo.
    echo [INFO] Application fermée normalement
)

endlocal
