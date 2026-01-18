@echo off
:: Script de test Python pour Windows
:: Diagnostique l'installation Python

echo ============================================
echo   Test Python pour Windows
echo ============================================
echo.

echo 1. Test avec 'python'...
python --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] 'python' fonctionne
    where python
) else (
    echo [ERREUR] 'python' ne fonctionne pas
)

echo.
echo 2. Test avec 'py' (Python Launcher)...
py --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] 'py' fonctionne
    where py
    echo.
    echo Versions Python installees:
    py --list
) else (
    echo [ERREUR] 'py' ne fonctionne pas
)

echo.
echo 3. Test avec 'python3'...
python3 --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] 'python3' fonctionne
    where python3
) else (
    echo [ERREUR] 'python3' ne fonctionne pas
)

echo.
echo 4. Verification de pip...
python -m pip --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] pip accessible via 'python -m pip'
) else (
    py -m pip --version 2>nul
    if %ERRORLEVEL% equ 0 (
        echo [OK] pip accessible via 'py -m pip'
    ) else (
        echo [ERREUR] pip n'est pas accessible
    )
)

echo.
echo 5. Verification de l'environnement virtuel...
if defined VIRTUAL_ENV (
    echo [OK] Vous etes dans un environnement virtuel
    echo VIRTUAL_ENV=%VIRTUAL_ENV%
) else (
    echo [INFO] Vous n'etes pas dans un environnement virtuel
)

echo.
echo 6. Variables d'environnement Python...
echo PATH:
echo %PATH% | findstr /i python

echo.
echo ============================================
echo   Fin du diagnostic
echo ============================================
echo.
pause
