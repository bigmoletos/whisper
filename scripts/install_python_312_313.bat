@echo off
echo ============================================
echo   Installation Python 3.12 et 3.13
echo ============================================
echo.

echo Les installateurs sont deja telecharges dans %TEMP%
echo.

echo [1/2] Installation de Python 3.12.9
echo.
echo Lancement de l'installateur Python 3.12.9
echo IMPORTANT: Cochez "Add Python to PATH" dans l'installateur
echo.
start /wait %TEMP%\python-3.12.9-amd64.exe

if %ERRORLEVEL% equ 0 (
    echo [OK] Python 3.12.9 installe
) else (
    echo [AVERTISSEMENT] Code retour: %ERRORLEVEL%
)
echo.
echo.

echo [2/2] Installation de Python 3.13.1
echo.
echo Lancement de l'installateur Python 3.13.1
echo IMPORTANT: Cochez "Add Python to PATH" dans l'installateur
echo.
start /wait %TEMP%\python-3.13.1-amd64.exe

if %ERRORLEVEL% equ 0 (
    echo [OK] Python 3.13.1 installe
) else (
    echo [AVERTISSEMENT] Code retour: %ERRORLEVEL%
)
echo.
echo.

echo ============================================
echo   Verification des installations
echo ============================================
echo.

echo Liste des versions Python:
py --list
echo.

echo Test Python 3.12:
py -3.12 --version
echo.

echo Test Python 3.13:
py -3.13 --version
echo.

echo ============================================
echo   Installation terminee
echo ============================================
echo.
echo Vous pouvez maintenant lancer:
echo   scripts\start_fast.bat
echo.

pause
