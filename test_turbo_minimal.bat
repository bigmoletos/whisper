@echo off
chcp 65001 >nul

echo ================================================
echo    TEST TURBO MINIMAL
echo ================================================
echo.

echo [INFO] Test avec version minimale de Voice-to-Text Turbo
echo [INFO] Cette version teste juste les imports sans lancer le service complet
echo.

py -3.12 turbo_minimal.py

echo.
echo [INFO] Test terminé. Code de sortie: %errorlevel%
pause