@echo off
setlocal enabledelayedexpansion

:: Script de lancement simple pour Whisper STT avec Faster-Whisper
:: Auteur: Bigmoletos
:: Date: 2026-01-18

title Whisper STT - Faster-Whisper

echo ============================================
echo   Whisper STT - Faster-Whisper
echo ============================================
echo.

:: Changer vers le répertoire racine du projet
cd /d "%~dp0.."

:: Vérifier Python - Priorité à Python 3.12 puis 3.11
echo Detection de Python
echo.

:: Essayer Python 3.12
echo Test Python 3.12
py -3.12 -c "print('OK')" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Python 3.12 trouve et fonctionnel
    py -3.12 --version
    set "PYTHON_CMD=py -3.12"
    goto :continue_script
)

:: Essayer Python 3.11 en fallback
echo Test Python 3.11
py -3.11 -c "print('OK')" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Python 3.11 trouve et fonctionnel
    py -3.11 --version
    set "PYTHON_CMD=py -3.11"
    goto :continue_script
)

echo [ERREUR] Python 3.12 ou 3.11 requis mais non trouve
echo.
echo Diagnostic:
py --list 2>nul
echo.
echo SOLUTIONS:
echo 1. Installez Python 3.12: https://www.python.org/downloads/
echo 2. OU utilisez: scripts\start.bat (accepte Python 3.10+)
echo.
pause
exit /b 1

:continue_script
echo.
echo Commande Python: !PYTHON_CMD!
echo.

:: Vérifier config.json
echo Verification de la configuration
!PYTHON_CMD! scripts\config_checker.py
if %ERRORLEVEL% neq 0 (
    echo [ERREUR] Probleme avec la configuration
    pause
    exit /b 1
)
echo.

:: Vérifier whisper et faster-whisper
echo Verification des modules whisper
!PYTHON_CMD! -c "import whisper" >nul 2>&1
set WHISPER_OK=%ERRORLEVEL%

!PYTHON_CMD! -c "import faster_whisper" >nul 2>&1
set FASTER_WHISPER_OK=%ERRORLEVEL%

if %WHISPER_OK% equ 0 if %FASTER_WHISPER_OK% equ 0 (
    echo [OK] whisper et faster-whisper sont installes
    goto :launch_app
)

if %WHISPER_OK% neq 0 (
    echo [INFO] openai-whisper n'est pas installe
)
if %FASTER_WHISPER_OK% neq 0 (
    echo [INFO] faster-whisper n'est pas installe
)
echo.

:: Détecter si on est dans un venv
if defined VIRTUAL_ENV (
    echo [INFO] Environnement virtuel detecte
    echo Installation de openai-whisper et faster-whisper en cours
    !PYTHON_CMD! -m pip install openai-whisper faster-whisper
    goto :check_install
)

echo Installation de openai-whisper et faster-whisper en mode utilisateur
!PYTHON_CMD! -m pip install openai-whisper faster-whisper --user

:check_install

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERREUR] Installation de whisper a echoue
    echo.
    echo SOLUTIONS:
    echo 1. Pour faster-whisper, installez Rust: https://rustup.rs/
    echo 2. OU changez config.json pour utiliser engine: whisper
    echo 3. Verifiez votre connexion internet
    echo.
    pause
    exit /b 1
)

echo.
echo Installation des dependances supplementaires
!PYTHON_CMD! -m pip install sounddevice numpy pywin32 pynput win10toast --user --quiet
if %ERRORLEVEL% neq 0 (
    echo [AVERTISSEMENT] Certaines dependances ont echoue
)

:launch_app
echo.
echo ============================================
echo   Demarrage de l'application
echo ============================================
echo.
echo Raccourci: Ctrl+Alt+7
echo Arret: Ctrl+C
echo.

!PYTHON_CMD! -m src.main

if %ERRORLEVEL% equ 0 (
    echo.
    echo [OK] Application terminee
) else (
    echo.
    echo [ERREUR] Erreur code: !ERRORLEVEL!
)

echo.
pause
