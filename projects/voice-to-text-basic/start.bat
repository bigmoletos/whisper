@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ================================================
echo    VOICE-TO-TEXT BASIC - Transcription Simple
echo    (Whisper Standard - CPU)
echo ================================================
echo.

:: Répertoire du projet
set "PROJECT_DIR=%~dp0"
set "ROOT_DIR=%PROJECT_DIR%..\.."
set "SHARED_DIR=%ROOT_DIR%\shared"
set "VENV_DIR=%ROOT_DIR%\venv_whisper"

:: Vérifier Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouvé. Veuillez installer Python 3.10+
    pause
    exit /b 1
)

:: Vérifier et créer/réparer l'environnement virtuel
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Activation de l'environnement virtuel...
    call "%VENV_DIR%\Scripts\activate.bat"

    :: Vérifier si pip fonctionne
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo [AVERTISSEMENT] Environnement virtuel corrompu détecté
        echo [INFO] Suppression et recréation de l'environnement virtuel...
        call deactivate 2>nul
        rmdir /s /q "%VENV_DIR%"
        python -m venv "%VENV_DIR%"
        call "%VENV_DIR%\Scripts\activate.bat"
    )
) else (
    echo [INFO] Création de l'environnement virtuel...
    python -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
)

:: Vérifier si les dépendances sont installées
python -c "import sounddevice" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dépendances requises...
    python -m pip install --upgrade pip
    python -m pip install -r "%ROOT_DIR%\requirements.txt"
    if errorlevel 1 (
        echo [ERREUR] Échec de l'installation des dépendances
        pause
        exit /b 1
    )
    echo [OK] Dépendances installées avec succès
)

:: Copier la config si nécessaire
if not exist "%SHARED_DIR%\src\config.json" (
    copy "%PROJECT_DIR%config.json" "%SHARED_DIR%\src\config.json" >nul
)

:: Lancer l'application
echo.
echo [INFO] Démarrage de Voice-to-Text Basic...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo.

cd /d "%SHARED_DIR%\src"
python main.py --config "%PROJECT_DIR%config.json"

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur
    pause
)

endlocal
