@echo off
REM Script d'installation du service Windows pour Whisper STT
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Installation Service Windows Whisper STT
echo ========================================
echo.
echo Ce script va installer Whisper STT comme service Windows
echo qui demarrera automatiquement au boot.
echo.
echo IMPORTANT: Ce script necessite des privileges administrateur
echo.

REM Vérifier les privilèges administrateur
net session >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Ce script doit etre execute en tant qu'administrateur
    echo Clic droit sur le fichier -^> Executer en tant qu'administrateur
    pause
    exit /b 1
)

cd /d "%~dp0.."

REM Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

echo [1/3] Installation de NSSM (Non-Sucking Service Manager)...
if not exist "nssm.exe" (
    echo Telechargement de NSSM...
    powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'"
    if errorlevel 1 (
        echo ERREUR: Echec du telechargement de NSSM
        echo Telechargez manuellement depuis https://nssm.cc/download
        pause
        exit /b 1
    )

    powershell -Command "Expand-Archive -Path 'nssm.zip' -DestinationPath '.' -Force"
    move "nssm-2.24\win64\nssm.exe" "nssm.exe" >nul 2>&1
    rmdir /s /q "nssm-2.24" >nul 2>&1
    del "nssm.zip" >nul 2>&1
)

echo [2/3] Configuration du service...
REM Désinstaller le service s'il existe déjà
nssm.exe stop WhisperSTT >nul 2>&1
nssm.exe remove WhisperSTT confirm >nul 2>&1

REM Installer le service
nssm.exe install WhisperSTT "python" "-m src.main"
if errorlevel 1 (
    echo ERREUR: Echec de l'installation du service
    pause
    exit /b 1
)

REM Configurer le service
nssm.exe set WhisperSTT AppDirectory "%CD%"
nssm.exe set WhisperSTT DisplayName "Whisper STT Global Service"
nssm.exe set WhisperSTT Description "Service de transcription vocale Whisper STT Global"
nssm.exe set WhisperSTT Start SERVICE_AUTO_START
nssm.exe set WhisperSTT AppStdout "%CD%\logs\service.log"
nssm.exe set WhisperSTT AppStderr "%CD%\logs\service_error.log"

REM Créer le dossier logs s'il n'existe pas
if not exist "logs" mkdir logs

echo [3/3] Demarrage du service...
nssm.exe start WhisperSTT

if errorlevel 1 (
    echo ATTENTION: Le service n'a pas pu demarrer automatiquement
    echo Vous pouvez le demarrer manuellement avec:
    echo   nssm.exe start WhisperSTT
    echo.
    echo Ou via les Services Windows (services.msc)
) else (
    echo Service demarre avec succes!
)

echo.
echo ========================================
echo Installation terminee!
echo ========================================
echo.
echo Le service WhisperSTT est maintenant installe et demarre au boot.
echo.
echo Commandes utiles:
echo   - Demarrer: nssm.exe start WhisperSTT
echo   - Arreter: nssm.exe stop WhisperSTT
echo   - Redemarrer: nssm.exe restart WhisperSTT
echo   - Desinstaller: nssm.exe remove WhisperSTT confirm
echo   - Status: nssm.exe status WhisperSTT
echo.
echo Logs disponibles dans: logs\service.log
echo.
pause
