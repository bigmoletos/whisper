@echo off
chcp 65001 >nul

echo ================================================
echo    TEST PYTHON DE BASE
echo ================================================
echo.

echo [1] Test Python 3.12...
py -3.12 --version
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé
    pause
    exit /b 1
)

echo.
echo [2] Test modules de base Python...
py -3.12 -c "import sys, json, logging, pathlib; print('[OK] Modules de base Python')"
if errorlevel 1 (
    echo [ERREUR] Modules de base Python manquants
    pause
    exit /b 1
)

echo.
echo [3] Test pip...
py -3.12 -m pip --version
if errorlevel 1 (
    echo [ERREUR] pip non fonctionnel
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Python 3.12 et pip fonctionnent correctement
echo [INFO] Vous pouvez maintenant installer les modules avec: install_modules_simple.bat
echo.
pause