@echo off
chcp 65001 >nul

echo ================================================
echo    TEST DIRECT - LANCEMENT MAIN.PY
echo ================================================
echo.

echo [INFO] Test de lancement direct de main.py
echo [INFO] Toutes les erreurs seront affichées
echo.

cd /d "%~dp0"
echo [DEBUG] Répertoire: %CD%
echo [DEBUG] Commande: py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json
echo.

py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json

echo.
echo [INFO] Code de sortie: %errorlevel%
echo [INFO] Appuyez sur une touche pour fermer...
pause >nul