@echo off
setlocal enabledelayedexpansion

echo === Test syntaxe batch ===
echo.

:: Test 1: Variable avec espace
set "PYTHON_CMD=py -3.11"
echo Test 1: !PYTHON_CMD!
!PYTHON_CMD! --version
echo ERRORLEVEL: !ERRORLEVEL!
echo.

:: Test 2: If defined avec goto
if defined VIRTUAL_ENV (
    echo Test 2: VIRTUAL_ENV defini
    goto :test3
)
echo Test 2: VIRTUAL_ENV non defini

:test3
echo.
echo Test 3: Appel Python
!PYTHON_CMD! scripts\config_checker.py
echo ERRORLEVEL: !ERRORLEVEL!
echo.

echo === Tous les tests OK ===
pause
