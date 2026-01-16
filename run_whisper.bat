@echo off
setlocal enabledelayedexpansion

:: Script de lancement de Whisper STT
:: Ce script configure l'environnement et lance l'application

title Whisper STT - Service de Transcription Vocale

:: Afficher le logo et les informations
echo ============================================
echo   Whisper STT - Service de Transcription Vocale
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

:: Configurer le chemin vers le répertoire src
set SCRIPT_DIR=%~dp0
set SRC_DIR=%SCRIPT_DIR%src

:: Ajouter le répertoire src au PYTHONPATH
set PYTHONPATH=%SRC_DIR%;%PYTHONPATH%

:: Vérifier les dépendances essentielles
echo Vérification des dépendances...
!PYTHON_EXE! check_dependencies.py
if !ERRORLEVEL! neq 0 (
    echo.
    echo ⚠️  Certaines dépendances sont manquantes ou l\'installation a échoué
    echo Veuillez installer manuellement les packages manquants
    goto :error
)

echo.
echo Démarrage de l'application Whisper STT...
echo.
echo Appuyez sur Ctrl+Alt+7 pour démarrer/arrêter l'enregistrement
echo Appuyez sur Ctrl+C dans cette fenêtre pour arrêter le service
echo.

:: Lancer l'application principale
!PYTHON_EXE! -m src.main

if !ERRORLEVEL! equ 0 (
    echo.
    echo L'application s'est terminée normalement
) else (
    echo.
    echo L'application s'est terminée avec des erreurs (code: !ERRORLEVEL!)
)

goto :end

:error
echo.
echo ⚠️  Erreur lors de la vérification des dépendances
echo Veuillez installer manuellement les packages manquants

:end
pause