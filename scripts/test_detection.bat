@echo off
setlocal enabledelayedexpansion

echo === Test detection Python 3.12 ===
echo.

echo Test 1: py -3.12 --version
py -3.12 --version
set ERROR1=!ERRORLEVEL!
echo ERRORLEVEL = !ERROR1!
echo.

echo Test 2: Verification du code retour
if !ERROR1! equ 0 (
    echo [OK] Python 3.12 trouve
) else (
    echo [ERREUR] Python 3.12 non trouve - Code: !ERROR1!
)
echo.

echo Test 3: py --list
py --list
echo.

echo Test 4: Verification simple
py -3.12 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Test simple reussi
) else (
    echo [ERREUR] Test simple echoue - Code: %ERRORLEVEL%
)
echo.

echo Test 5: Sans redirection
py -3.12 --version
if %ERRORLEVEL% equ 0 (
    echo [OK] Sans redirection reussi
) else (
    echo [ERREUR] Sans redirection echoue - Code: %ERRORLEVEL%
)

pause
