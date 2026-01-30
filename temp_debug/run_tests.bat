@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo [INFO] Lancement des tests VTT...
echo.

cd /d "%~dp0.."

REM Vérifier si pytest est installé
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] pytest non installé, installation...
    pip install pytest
    if errorlevel 1 (
        echo [ERROR] Impossible d'installer pytest
        exit /b 1
    )
)

REM Vérifier si le répertoire tests existe
if not exist "tests" (
    echo [INFO] Répertoire tests non trouvé, création...
    mkdir tests
    echo # Tests VTT > tests\__init__.py
)

REM Lancer les tests avec options appropriées
echo [INFO] Exécution des tests...
python -m pytest tests/ -v --tb=short -q --disable-warnings
set TEST_RESULT=%errorlevel%

if %TEST_RESULT% equ 0 (
    echo.
    echo [OK] Tous les tests sont passés
) else (
    echo.
    echo [WARNING] Certains tests ont échoué (code: %TEST_RESULT%)
)

echo.
echo === System Health Check Complete ===
exit /b %TEST_RESULT%