@echo off
echo === Diagnostic Python 3.12 ===
echo.

echo Test 1: py --list
py --list
echo.

echo Test 2: py -3.12 --version
py -3.12 --version
echo Code sortie: %ERRORLEVEL%
echo.

echo Test 3: Recherche python.exe directement
where python
echo.

echo Test 4: python3 --version
python3 --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] python3 fonctionne
) else (
    echo [ERREUR] python3 ne fonctionne pas
)
echo.

echo Test 5: python --version
python --version
echo Code sortie: %ERRORLEVEL%
echo.

pause
