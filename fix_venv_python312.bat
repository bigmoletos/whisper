@echo off
chcp 65001 >nul

echo ================================================
echo    CORRECTION ENVIRONNEMENT VIRTUEL PYTHON 3.12
echo ================================================
echo.

:: Répertoire du projet
set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%venv_whisper"

:: Vérifier Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé. Versions disponibles :
    py -0 2>nul
    echo [INFO] Appuyez sur une touche pour fermer...
    pause >nul
    exit /b 1
)
echo [OK] Python 3.12 détecté

:: Supprimer l'ancien environnement virtuel
if exist "%VENV_DIR%" (
    echo [INFO] Suppression de l'ancien environnement virtuel...
    rmdir /s /q "%VENV_DIR%" 2>nul
    if exist "%VENV_DIR%" (
        echo [WARNING] Impossible de supprimer complètement l'ancien environnement
        echo [INFO] Tentative de suppression forcée...
        timeout /t 2 >nul
        rmdir /s /q "%VENV_DIR%" 2>nul
    )
)

:: Créer un nouvel environnement virtuel avec Python 3.12
echo [INFO] Création d'un nouvel environnement virtuel avec Python 3.12...
py -3.12 -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ERREUR] Échec de création de l'environnement virtuel
    echo [INFO] Appuyez sur une touche pour fermer...
    pause >nul
    exit /b 1
)

echo [OK] Nouvel environnement virtuel créé avec Python 3.12

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

:: Installer les dépendances de base
echo [INFO] Installation des dépendances de base...
python -m pip install sounddevice numpy torch

echo.
echo [OK] Environnement virtuel Python 3.12 configuré avec succès !
echo [INFO] Vous pouvez maintenant utiliser Voice-to-Text Turbo
echo.
pause