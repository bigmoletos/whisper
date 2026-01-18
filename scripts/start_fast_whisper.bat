@echo off
setlocal enabledelayedexpansion

:: Script de lancement de Whisper STT avec Faster-Whisper (version rapide)
:: Ce script configure l'environnement et lance l'application avec Faster-Whisper

title Whisper STT - Faster-Whisper (Version Rapide)

:: Afficher le logo et les informations
echo ============================================
echo   Whisper STT - Faster-Whisper (Version Rapide)
echo ============================================
echo.

:: Vérifier et configurer l'environnement Python
set PYTHON_EXE=python
where !PYTHON_EXE! >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo Erreur: Python n'est pas installé ou n'est pas dans le PATH
    pause
    exit /b 1
)

:: Changer vers le répertoire racine du projet (parent du dossier scripts)
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

:: Vérifier la version de Python
echo Vérification de la version de Python...
!PYTHON_EXE! check_python_version.py
if !ERRORLEVEL! neq 0 (
    echo.
    echo ⚠️  Version de Python incompatible
    echo Veuillez installer Python 3.10 ou supérieur (recommandé: 3.11 ou 3.12)
    pause
    exit /b 1
)

:: Vérifier que faster-whisper est installé
echo Vérification de Faster-Whisper...
!PYTHON_EXE! -c "import faster_whisper; print('Faster-Whisper est installé')" 2>nul
if !ERRORLEVEL! neq 0 (
    echo.
    echo ⚠️  Faster-Whisper n'est pas installé
    echo.
    echo Installation de Faster-Whisper en cours...
    echo (Cela peut prendre quelques minutes, surtout si Rust n'est pas installé)
    echo.
    !PYTHON_EXE! -m pip install faster-whisper
    if !ERRORLEVEL! neq 0 (
        echo.
        echo ❌ Échec de l'installation de Faster-Whisper
        echo.
        echo Faster-Whisper nécessite Rust pour être compilé.
        echo Veuillez installer Rust depuis https://rustup.rs/
        echo ou exécutez: scripts\install_rust.bat
        echo.
        pause
        exit /b 1
    )
    echo.
    echo ✅ Faster-Whisper installé avec succès
    echo.
)

:: Vérifier les dépendances essentielles
echo Vérification des autres dépendances...
!PYTHON_EXE! check_dependencies.py
if !ERRORLEVEL! neq 0 (
    echo.
    echo ⚠️  Certaines dépendances sont manquantes ou l'installation a échoué
    echo Veuillez installer manuellement les packages manquants
    goto :error
)

:: Configurer le chemin vers le répertoire src
set SRC_DIR=%PROJECT_ROOT%\src

:: Ajouter le répertoire src au PYTHONPATH
set PYTHONPATH=%SRC_DIR%;%PYTHONPATH%

:: Sauvegarder le config.json actuel si nécessaire
set CONFIG_BACKUP=%TEMP%\whisper_config_backup_%RANDOM%.json
if exist "config.json" (
    copy "config.json" "!CONFIG_BACKUP!" >nul 2>&1
)

:: Forcer l'utilisation de faster-whisper dans la configuration
echo.
echo Configuration pour utiliser Faster-Whisper...
!PYTHON_EXE! -c "import json; config = json.load(open('config.json', 'r', encoding='utf-8')); config['whisper']['engine'] = 'faster-whisper'; json.dump(config, open('config.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)" 2>nul
if !ERRORLEVEL! neq 0 (
    echo ⚠️  Impossible de modifier config.json, utilisation de la configuration existante
)

echo.
echo ============================================
echo   Démarrage avec Faster-Whisper
echo ============================================
echo.
echo 🚀 Moteur: Faster-Whisper (version optimisée)
echo 📝 Raccourci: Ctrl+Alt+7 (configurable dans config.json)
echo ⏹️  Arrêt: Ctrl+C dans cette fenêtre
echo.
echo 💡 Astuce: Faster-Whisper est plus rapide que Whisper standard
echo    et utilise moins de mémoire grâce à l'optimisation CTranslate2
echo.

:: Lancer l'application principale
!PYTHON_EXE! -m src.main

:: Restaurer le config.json si sauvegardé
if exist "!CONFIG_BACKUP!" (
    move /Y "!CONFIG_BACKUP!" "config.json" >nul 2>&1
)

if !ERRORLEVEL! equ 0 (
    echo.
    echo ✅ L'application s'est terminée normalement
) else (
    echo.
    echo ❌ L'application s'est terminée avec des erreurs (code: !ERRORLEVEL!)
)

goto :end

:error
echo.
echo ⚠️  Erreur lors de la vérification des dépendances
echo Veuillez installer manuellement les packages manquants

:end
echo.
pause
