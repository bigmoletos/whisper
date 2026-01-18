@echo off
setlocal enabledelayedexpansion

:: Script de lancement FAST v2 - Detection amelioree
:: Auteur: Bigmoletos
:: Date: 2026-01-18

title Whisper STT - Faster-Whisper

echo ============================================
echo   Whisper STT - Faster-Whisper v2
echo ============================================
echo.

:: Changer vers le répertoire racine du projet
cd /d "%~dp0.."

:: Vérifier Python 3.12 via py --list
echo Detection de Python 3.12
echo.

py --list 2>nul | findstr /C:"3.12" >nul
if %ERRORLEVEL% neq 0 (
    echo [ERREUR] Python 3.12 non trouve dans py --list
    echo.
    echo Liste des versions disponibles:
    py --list
    echo.
    echo SOLUTIONS:
    echo 1. Installez Python 3.12: https://www.python.org/downloads/
    echo 2. OU utilisez: scripts\start.bat (accepte Python 3.10+)
    echo.
    pause
    exit /b 1
)

echo [INFO] Python 3.12 trouve dans la liste
echo.

:: Tester si py -3.12 fonctionne réellement
echo Test execution Python 3.12
for /f "delims=" %%i in ('py -3.12 -c "import sys; print(sys.version)" 2^>nul') do (
    set PYTHON_VERSION=%%i
    goto :python_ok
)

echo [ERREUR] Python 3.12 est liste mais ne peut pas s'executer
echo.
echo Cela signifie que votre installation Python 3.12 est corrompue
echo.
echo SOLUTIONS:
echo 1. Desinstallez Python 3.12
echo 2. Reinstallez Python 3.12: https://www.python.org/downloads/
echo 3. OU utilisez: scripts\start.bat (essaie Python 3.10+)
echo.
pause
exit /b 1

:python_ok
echo [OK] Python 3.12 fonctionne
echo Version: !PYTHON_VERSION!
set "PYTHON_CMD=py -3.12"
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

:: Vérifier faster-whisper
echo Verification de faster-whisper
!PYTHON_CMD! -c "import faster_whisper" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] faster-whisper est installe
    goto :launch_app
)

echo [INFO] faster-whisper n'est pas installe
echo.

:: Détecter si on est dans un venv
if defined VIRTUAL_ENV (
    echo [INFO] Environnement virtuel detecte
    echo Installation de faster-whisper en cours
    !PYTHON_CMD! -m pip install faster-whisper
    goto :check_install
)

echo Installation de faster-whisper en mode utilisateur
!PYTHON_CMD! -m pip install faster-whisper --user

:check_install

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERREUR] Installation de faster-whisper a echoue
    echo.
    echo SOLUTIONS:
    echo 1. Installez Rust: https://rustup.rs/
    echo 2. OU changez config.json pour utiliser engine: whisper
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
