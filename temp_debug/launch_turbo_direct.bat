@echo off
chcp 65001 >nul

echo ================================================
echo    VOICE-TO-TEXT TURBO - LANCEMENT DIRECT
echo ================================================
echo.

echo [INFO] Lancement direct de Voice-to-Text Turbo
echo [INFO] Contournement du menu pour éviter les problèmes
echo.

:: Aller dans le bon répertoire
cd /d "%~dp0"

echo [DEBUG] Répertoire: %CD%
echo [DEBUG] Commande: py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json
echo.

echo [INFO] Démarrage de Voice-to-Text Turbo...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo [INFO] Appuyez sur Ctrl+C pour arrêter
echo.

:: Lancer directement l'application
py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json

echo.
echo [INFO] Application fermée
pause